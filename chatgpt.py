import requests
import streamlit as st

def gpt_ask(question):
    url = "http://18.144.49.204:8060/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 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"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that provides information about banking services. Please start your answer with '尊敬的用户您好！' and then go to a new paragraph"},
            {"role": "user", "content": question}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()

    return response_json['choices'][0]['message']['content']


def gpt_thanks(user, prize):
    url = "http://18.144.49.204:8060/v1/chat/completions"
    content = f"请为用户{user}写一封感谢信，告知他抽到的奖品是{prize}，向他介绍一下这个奖品，并且感谢用户对本银行的支持。回答以‘尊敬的用户{user}’开头，结尾的落款是‘兴业银行’"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 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"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system",
             "content": "You are a helpful assistant that provides information about users' prizes and thanks letter."},
            {"role": "user", "content": content}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()

    return response_json['choices'][0]['message']['content']

def gpt_intro(function):
    url = "http://18.144.49.204:8060/v1/chat/completions"
    content = f"以兴业银行工作人员的语气向用户介绍兴业银行的{function}这个部门或服务或设施作为用户导览。"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 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"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that provides information about banking services. Please start your answer with '尊敬的用户您好！' and then go to a new paragraph"},
            {"role": "user", "content": content}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()

    return response_json['choices'][0]['message']['content']

st.title("智能助手")

selected_option = st.radio("有什么可以为您服务:", ["小兴问答", "业务导览"])

if selected_option == "小兴问答":
    st.write("欢迎进入小兴问答！")
    user_question = st.text_input("请输入您的问题：")
    if user_question:
        answer = gpt_ask(user_question)
        st.write(answer)

elif selected_option == "业务导览":
    st.write("欢迎进入业务导览！")

    import streamlit as st

    # 创建三列布局
    col1, col2, col3 = st.columns(3)

    # 在每列中添加按钮
    with col1:
        department_button = st.button("部门导览")


    with col2:
        service_button = st.button("服务导览")


    with col3:
        device_button = st.button("设备导览")


    # 判断按钮是否被点击并显示对应信息
    if department_button:
        st.write("您选择了：部门导览")
        # 在这里添加部门导览的信息
        select1 = st.radio("请选择一个部门：",['个人储蓄与支票账户部门', '信用卡部门', '投资与理财部门'])
        if select1:
            a = gpt_intro(select1)
            st.write(a)

    if service_button:
        st.write("您选择了：服务导览")
        # 在这里添加服务导览的信息
        select2 = st.radio("请选择一个服务：",['个人账户管理', '贷款申请', '投资咨询'])
        if select2:
            a = gpt_intro(select2)
            st.write(a)

    if device_button:
        st.write("您选择了：设备导览")
        # 在这里添加设备导览的信息
        select3 = st.radio("请选择一个设施：",['自动取款机', '会议室'])
        if select3:
            a = gpt_intro(select3)
            st.write(a)
