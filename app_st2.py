import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import random


st.title("赵氏集团公司首页")
st.header("为赵氏总裁赵超振量身打造的宝宝乐园")
st.write("")
st.write("")
st.write("")


st.subheader("I. 选择一个身份吧")
#caidan = st.selectbox([0,1,2,3])

# 定义角色和对应的图片
roles = ['赵德德', '赵sese', '兔子精', '赵宝宝']
images = {
'赵德德': 'image1.png',
'赵sese': 'image2.png',
'兔子精': 'image3.png',
'赵宝宝': 'image4.png'
}

descriptions = {
    '赵德德': '生子当如赵德德，日窥明镜自琢磨。\n\n快拨慢捻抹复挑，乐游原上与君和。',
    '赵sese': '哥哥~~鬼节可以sese，不可以发抖哦~~略略略~',
    '兔子精': '祝小兔子精生日快乐，精力旺盛不虚弱！！嘿嘿~嘻嘻~',
    '赵宝宝': '上元节到中元节，匆匆已是半载。待到新年，就能一起看雪花飘落吧！\n\n从一面惊鸿到夜夜入梦，仿佛前生已相逢。\n\n你让我相信当真有命中注定，你的爱给我安心和快乐，我爱你的成熟稳重，也喜欢你像小孩一般无忧无虑的天真。\n\n赵宝宝，愿我可以做你的港湾，愿你永远是旺财小可爱(✿◕‿◕✿)'
}

st.session_state.role = st.selectbox('请总裁选择一个角色:', roles)

# 添加确认按钮
if st.button('就这个啦'):

    if st.session_state.role == '赵宝宝':
      st.write('')
      st.snow()
    else:
      st.write(f'您选择的角色是{st.session_state.role}，以下是为你定制的祝福！')
      st.balloons()

    # 显示用户选择的角色对应的图片
    if st.session_state.role:
        image = Image.open(images[st.session_state.role])
        image = image.resize((500, 500))
        st.image(image, caption=st.session_state.role, use_column_width=True)

    if st.session_state.role in descriptions:
        #st.markdown(f"<p style='color:blue;font-size:20px;'>{descriptions[role]}</p>", unsafe_allow_html=True)
        description = descriptions[st.session_state.role]
        # gradient_description = ""
        # for char in description:
        #     gradient_description += f"<span style='color:hsl({ord(char) % 360}, 70%, 50%);'>{char}</span>"
        # st.markdown(f"<p style='font-size:20px;font-family:LiSu'>{gradient_description}</p>", unsafe_allow_html=True)
        des = description.split('\n\n')
        for d in des:
          st.markdown(f"<p style='font-size:30px;font-family:LiSu;'><span class='rainbow-text'>{d}</span></p>",
                    unsafe_allow_html=True)






st.write("")
st.subheader("II. 普天之下，莫非赵土")
st.subheader("     ——总裁和总裁夫人曾经走过盛世江山")
st.write("当你谈论我们的爱情，就不能只谈爱情。\n\n你要记得料峭初春的风筝，烟火如昼的花灯，开封古城的斗鸡，秦淮河畔的雨声。\n\n你要记得每个周末的清晨微风，和放歌骑车的街头夜行。\n\n还有我的哼哼哼和嘤嘤嘤~~~")
df = pd.DataFrame(
     np.array([[34.793,114.335],[34.6478,115.16],[34.62,112.45],[34.384,115.61],[32.06,118.81],[31.95,118.815],[
  31.236320019680164,
  121.44980494083192
],[
  31.019628027092494,
  121.60733789045865
],[
  31.316582547562675,
  121.51714004954033
],[
  31.3780988805043,
  121.19435457414647
],[
  31.33598241480193,
  121.31359262083288
],[
    32.025265332723755,
    118.78863103312226
  ],
  [
    32.03989680162723,
    118.78739831051536
  ],
  [
    32.03954919979214,
    118.78483632619682
  ],
  [
    32.038760969184615,
    118.78706950908963
  ],
  [
    32.030099573615026,
    118.80055588281233
  ],
  [
    32.0305965139379,
    118.79929149919346
  ],
  [
    32.0257955031256,
    118.78856421480819
  ],
  [
    32.040450978638944,
    118.7853702047128
  ],
  [
    32.039724203118624,
    118.7861660404417
  ],
  [
    32.039181767581475,
    118.78555839855332
  ],[
    34.66792358168227,
    112.38942414193708
  ],
  [
    34.63322984333986,
    112.45282161923863
  ],
  [
    34.66983886514531,
    112.38449765666478
  ],
  [
    34.62754496116479,
    112.45472500694576
  ],
  [
    34.672678575314016,
    112.3893402232135
  ],
  [
    34.67053570985749,
    112.47654201726652
  ],
  [
    34.68124842015025,
    112.3934836434917
  ],
  [
    34.628237052654946,
    112.44761330999104
  ],
  [
    34.67238697850819,
    112.390119108366
  ],
  [
    34.66496836291181,
    112.47539034901894
  ],[
    34.80795953073822,
    114.34510753958841
  ],
  [
    34.818042789146375,
    114.35224219672949
  ],
  [
    34.809410302557374,
    114.34177114503383
  ],
  [
    34.80957025905767,
    114.33787373065566
  ],
  [
    34.806173222543364,
    114.33904055902549
  ],
  [
    34.81075359225865,
    114.34084858287528
  ],
  [
    34.81502309429017,
    114.33960508277667
  ],
  [
    34.81681438974211,
    114.33173502172339
  ],
  [
    34.81631012287141,
    114.34970708992188
  ],
  [
    34.812535772579764,
    114.34212402724854
  ],[
    34.3896419188649,
    115.60799148587647
  ],
  [
    34.38538723951064,
    115.6037596079923
  ],
  [
    34.37906400269236,
    115.60670487794004
  ],
  [
    34.386017366497635,
    115.61121759790453
  ],[
    31.338968388601142,
    121.4950172490241
  ],
  [
    31.339847168382896,
    121.49729572683613
  ],
  [
    31.33747684782943,
    121.49579865387564
  ],
  [
    31.339468965045228,
    121.49737519056238
  ],
  [
    31.302262601955967,
    121.22855279588255
  ],
  [
    31.29986049656816,
    121.23062666086993
  ],
  [
    31.302409618779752,
    121.22852252696971
  ],
  [
    31.29930302178778,
    121.23592872018041
  ],
  [
    31.359998709944783,
    121.47435819428526
  ],
  [
    31.35976739011922,
    121.47525052119008
  ],
  [
    31.35967568349872,
    121.47344649472984
  ],
  [
    31.359001704532588,
    121.48012390885218
  ],
  [
    31.147385438758825,
    121.6588188371684
  ],
  [
    31.14868162753109,
    121.6592040175307
  ],
  [
    31.144529519405545,
    121.66387231612875
  ],
  [
    31.154387489656642,
    121.66360280267834
  ]]),
     columns=['lat', 'lon'])
st.map(df)

st.write("")
st.write("")
st.subheader("记忆游戏@之-总裁语录填空")
# 游戏数据
questions = [
    {
        "prompt": "电话吗？不打啦！____，然后拒绝。",
        "answer": "挑逗"
    },
    {
        "prompt": "明天穿大裤衩子，但不妨碍的嘚瑟，也就你了，那个让我____的女人。",
        "answer": "脱掉衣服"
    },
    {
        "prompt": "你看看你多少优势 狂吃不胖，脸还小 眼睛怎么用都不近视 还上那么好的学校 还____。",
        "answer": "找了个这么好的男朋友"
    },
    {
        "prompt": "看来只有我能让你每天____。",
        "answer": "洗澡"
    },
    {
        "prompt": "今天天气真舒服，如果这时候____溜达溜达，就会让人觉得，人间值得。",
        "answer": "牵上你的手"
    },
    {
        "prompt": "花卷，花卷你好，我是____。",
        "answer": "花菜"
    }
]

# 初始化状态
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
    st.session_state.correct_answers = 0

# 获取当前问题
current_question = questions[st.session_state.current_question_index]

# 显示问题提示
st.write("Question:", current_question["prompt"])

# 用户输入答案
user_input = st.text_input("Your answer:")

# # 检查答案
# if user_input.lower() == current_question["answer"].lower():
#     st.write("呦，记得挺清呀!")
#     st.session_state.correct_answers += 1
#     st.session_state.current_question_index += 1
# else:
#     st.write("小笨蛋，再来!")
#
# # 显示用户得分
# st.write("Correct answers:", st.session_state.correct_answers)
#
# # 显示下一个问题按钮
# if st.session_state.current_question_index < len(questions) - 1:
#     if st.button("Next Question"):
#         st.session_state.current_question_index += 1
# else:
#     st.write("Game Over!")

# 显示确认按钮
confirm_button = st.button("毛闷台")
flag = True

if confirm_button:
    if user_input.lower() == current_question["answer"].lower():
        st.write("呦，记得挺清呀!")
        st.session_state.correct_answers += 1
        st.session_state.current_question_index += 1
        user_input = ""  # 清空用户输入
    else:
        st.write("小笨蛋，再来!")
        flag = False

# 显示用户得分
# st.write("Correct answers:", st.session_state.correct_answers)

# 显示下一个问题按钮
if st.session_state.current_question_index < len(questions) and flag == True:
    next_button = st.button("Next Question")
    if next_button:
        st.session_state.current_question_index += 1
if st.session_state.current_question_index == len(questions):
    st.write("恭喜老公！闯关成功！")

# for i in range(6):
#   current_question = questions[i]
#   st.write("Question:", current_question["prompt"])

# keys = ["你猜是啥",'略略略',"来呀","快回答","嘿嘿嘿嘿","哼哼哼"]
#
# i = 0
# flag = True
# while i<6:
#   current_question = questions[i]
#
#   st.write("Question:", current_question["prompt"])
#   #flag = False
#   #key = 'key'+str(i)
#   user_input = st.text_area(keys[i], key=keys[i])
#   if user_input.lower() == current_question["answer"].lower():
#     st.write("呦，记得挺清呀!")
#     i += 1
#     #flag = True
#   else:
#     st.write("小笨蛋，再来!")
#
# if i == 6:
#   st.write("恭喜老公！闯关成功！")