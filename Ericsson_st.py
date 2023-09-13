import streamlit as st
import os
from zipfile import ZipFile
import re
import pandas as pd
from datetime import datetime

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

def extract_pdf(filename):
    # 用文件对象来创建一个pdf文档分析器
    praser = PDFParser(open(filename,'rb'))

    # 创建一个PDF文档
    doc = PDFDocument()

    # 连接分析器与文档对象
    praser.set_document(doc)
    doc.set_parser(praser)

    # 提供初始化密码，如果没有密码，就创建一个空的字符串
    doc.initialize()

    # result = {}
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        #创建PDF资源管理器，来管理共享资源
        rsrcmagr = PDFResourceManager()
        #创建一个PDF设备对象
        laparams = LAParams()
        #将资源管理器和设备对象聚合
        device = PDFPageAggregator(rsrcmagr, laparams=laparams)
        #创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmagr, device)

         # 只处理第一页
        pg = next(doc.get_pages())
        interpreter.process_page(pg)
        #接收该页面的LTPage对象
        layout = device.get_result()
        page_text = ""
        for x in layout:
            if (isinstance(x,LTTextBox)):
                page_text += x.get_text()
        #result[filename[-6:] + "_page0"] = page_text

    return page_text

def find_num(string):
    pattern = r'\b\d+(?:[.,]\d+)*\b'
    matches = re.findall(pattern, string)
    matches = [m for m in matches if ',' in m or '.' in m]
    matches = [m for m in matches if m.count('.')<=1]
    matches = list(set(matches))
    m2 = []
    for i in range(len(matches)):
        m = matches[i]
        if ',' in m:
            m2.append(m)
        if '.' in m and len(m)-m.index('.')==3:
            m2.append(m)
    m2 = list(set(m2))
    m2 = [int(''.join(filter(str.isdigit, s))) for s in m2]
    m2 = [x for x in m2 if x != max(m2)]

    u = None
    q = None

    if len(m2)==2:
        f1 = str(m2[0])[-2:] == '00'
        f2 = str(m2[1])[-2:] == '00'
        if f1 and not f2:
            q = m2[0]/100
            u = m2[1]/100
        elif not f1 and f2:
            q = m2[1]/100
            u = m2[0]/100
        else:
            u = min(m2[0], m2[1])/100
            q = max(m2[0], m2[1])/100

    if u is not None:
        u = f"{u:.2f}"
    if q is not None:
        q = f"{q:.2f}"

    return u, q


def extract_for_table(content):
    pattern1 = r"Date\n(\d{2}\.\d{2}\.\d{4})"
    pattern2 = r"Delivery Date\n(\d{2}\.\d{2}\.\d{4})"
    pattern3 = r"Purchase Order\n(\d{10})"
    pattern4 = r"Total net item value excl. tax (\S+)"
    # pattern5 = r"\npiece\s*\n\s*([\d,\.]+)\s*"
    # pattern6 = r"([A-Z]{3}\d+/+\w*)\n\s*([\d,]+\.\d+)\s*\n"
    pattern7 = r'Terms Of Delivery\n([A-Z]{3})'
    pattern8 = r'Buyer\n(.*?)\n'
    pattern9 = r'Delivery Address\n(.*?)\n'
    pattern10 = r'[A-Z]+\d+/\d+[A-Z\d]*'

    match1 = re.search(pattern1, content)
    match2 = re.search(pattern2, content)
    match3 = re.search(pattern3, content)
    match4 = re.search(pattern4, content)
    # match5 = re.search(pattern5, content)
    # match6 = re.search(pattern6, content)
    match7 = re.search(pattern7, content)
    match8 = re.search(pattern8, content)
    match9 = re.search(pattern9, content)
    match10 = re.search(pattern10, content)

    Order_Date = None
    Delivery_Date = None
    Purchase_Order = None
    Tax = None
    # Price_Unit = None
    # Quantity = None
    Product_No = None
    Term = None
    Buyer = None
    Address = None

    Price_Unit, Quantity = find_num(content)

    if match1:
        Order_Date = match1.group(1)
    if match2:
        Delivery_Date = match2.group(1)
    if match3:
        Purchase_Order = match3.group(1)
    if match4:
        Tax = match4.group(1)
    # if match5:
    #     Price_Unit = match5.group(1)
    # if match6:
    #     Quantity = match6.group(2)
    #     #Product_No = match6.group(1)
    if match7:
        Term = match7.group(1)
    if match8:
        Buyer = match8.group(1)
    if match9:
        Address = match9.group(1)
    if match10:
        Product_No = match10.group()

    return [Order_Date, Buyer, Product_No, Purchase_Order, Quantity, Address, Term, Tax, Delivery_Date, Price_Unit]

def jabil_table(contents):
    Order_Date = None
    Delivery_Date = None
    Purchase_Order = None
    Tax = None
    Price_Unit = None
    Quantity = None
    Product_No = None
    Term = None
    Buyer = None
    Address = None

    match1 = re.search(r'(\d+)\s*/\s*(\d{2}/\d{2}/\d{4})', contents)
    if match1:
        Purchase_Order = match1.group(1)
        Order_Date = match1.group(2)

    match2 = re.search(r'Terms of delivery:\s*([A-Z]{3})', contents)
    if match2:
        Term = match2.group(1)

    match3 = re.search(r'\b([A-Z_]+)@JABIL\.COM', contents, re.IGNORECASE)
    if match3:
        Buyer = match3.group(1)
        Buyer = Buyer.replace('_', ' ')

    date_pattern = r'\d{2}/\d{2}/\d{4}'
    dates = re.findall(date_pattern, contents)

    if dates:
        # 将日期字符串转换为日期对象，并找到最晚的日期
        date_objects = [datetime.strptime(date, '%m/%d/%Y') for date in dates]
        latest_date = max(date_objects)
        Delivery_Date = latest_date.strftime('%m/%d/%Y')

    match4 = re.search(r'[A-Z]+[0-9]+/[0-9A-Za-z\-]+', contents)
    if match4:
        Product_No = match4.group()

    match5 = re.search(r'Total net value excl\. tax\s+([A-Z]{3})', contents, re.IGNORECASE)
    if match5:
        # 提取匹配到的连续三个大写字母
        Tax = match5.group(1)

    input_text = contents
    due_date_index = input_text.find("Due Date")
    #print(due_date_index)
    if due_date_index != -1:
        # 寻找第一个到第五个"\n"之间的内容
        input_text = input_text[due_date_index:]
        newline_positions = [pos for pos, char in enumerate(input_text) if char == '\n']
        if len(newline_positions) >= 5:
            start_index = newline_positions[0] + 1  # 第一个"\n"之后的索引
            end_index = newline_positions[4]  # 第五个"\n"之前的索引
            extracted_text = input_text[start_index:end_index].strip()  # 提取并去除首尾空格

            # 将提取的内容以列表形式存储并一起打印
            extracted_list = extracted_text.split('\n')
            Quantity = extracted_list[0]
            Price_Unit = extracted_list[-1]

    return [Order_Date, Buyer, Product_No, Purchase_Order, Quantity, Address, Term, Tax, Delivery_Date, Price_Unit]


# 创建一个文件上传组件
uploaded_file = uploaded_files = st.file_uploader("上传多个文件或一个文件夹", type=["pdf"], accept_multiple_files=True)

if uploaded_file is not None:
    contents = []
    for uploaded_file in uploaded_files:
        # 读取每个上传文件的文件名
        file_name = uploaded_file.name
        res = extract_pdf(file_name)
        contents.append(res)
        # st.write(file_name)
        # st.write(f"上传的文件：{res[0:100]}")

    # for c in contents:
    #     res = extract_for_table(c)

    df = pd.DataFrame(columns=["订单时间", "Customer", "PN", "订单号码", "数量", "发货地址", "条款", "币种", "客户要求时间", "单价"])
    selected_customer = st.radio("选择客户:", ["Ericsson", "Jabil"])

    if selected_customer == "Ericsson":
        for content in contents:
            result = extract_for_table(content)
            df = df.append(pd.Series(result, index=df.columns), ignore_index=True)

    if selected_customer == "Jabil":
        for content in contents:
            result = jabil_table(content)
            df = df.append(pd.Series(result, index=df.columns), ignore_index=True)

    st.dataframe(df)

    if st.button("下载为Excel"):
        # 设置下载文件的名称
        file_name = "data.xlsx"

        # 使用pandas将数据框保存为Excel文件
        with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Sheet1', index=False)

        # 读取文件内容
        with open(file_name, 'rb') as file:
            data = file.read()

        # 生成下载链接
        st.download_button(label="点击下载Excel文件", data=data, file_name=file_name, key="download_excel")
