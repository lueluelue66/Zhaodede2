import streamlit as st

import pygame as py
import sys, random, time, os
import math
import numpy as np


# 预加载分数图
def pre_load_image(background):
    imageList = {}
    imagePath = './素材/分数/'
    image_filenames = [i for i in os.listdir(imagePath)]
    width = math.floor(background.width * (1 - internalWidth) / 4)
    for name in image_filenames:
        image = py.transform.smoothscale(py.image.load(imagePath + name).convert_alpha(), (width, width))
        imageList[name.replace('.png', '')] = image
    return imageList


# 加载分数图像
def draw_image(score_list, image_list, pos_list):
    for pos_num in score_list:
        score = score_list[pos_num]
        scoreSurf = BasicFont01.render('{}'.format(score), True, (0, 0, 0))
        scoreRect = scoreSurf.get_rect()
        if score <= 4096:
            image = image_list['{}'.format(score)]
        else:
            image = image_list['4096']
        imageRect = image.get_rect()
        imageRect.topleft = pos_list['{}'.format(pos_num)]
        scoreRect.center = imageRect.center
        screen.blit(image, imageRect)
        if score > 0:
            screen.blit(scoreSurf, scoreRect)


# 图像位置列表，表示为(x,y)
# 用于确定加载的分数图像的显示点位
def image_pos_list(background):
    pre_x = background.topleft[0]
    pre_y = background.topleft[-1]
    internalLong = math.ceil(internalWidth / 5 * background.width)
    imageLong = math.floor((1 - internalWidth) / 4 * background.width)
    posList = dict(zip(list(range(1, 17)), [''] * 16))
    for num in range(1, 17):
        row1, row2 = divmod(num, 4)
        row = row1 + np.sign(row2)
        column = [row2 if row2 != 0 else 4][0]
        image_x = pre_x + internalLong * column + imageLong * (column - 1)
        image_y = pre_y + internalLong * row + imageLong * (row - 1)
        posList['{}'.format(num)] = (image_x, image_y)
    return posList


# 预加载移动逻辑
def pre_move():
    numberPos = {}
    for num in range(1, 17):
        row1, row2 = divmod(num, 4)
        row = row1 + np.sign(row2)
        column = [row2 if row2 != 0 else 4][0]
        numberPos['{}'.format([row, column])] = num

    return numberPos


# 移动逻辑
def number_move(number_pos, move_input, score_list):
    values = list(number_pos.values())
    keys = list(number_pos.keys())
    numberPosReverse = dict(zip(values, keys))
    newScoreList = score_list.copy()
    oldScoreList = {}
    while newScoreList != oldScoreList:
        oldScoreList = newScoreList.copy()
        for num in range(1, 17):
            pos = eval(numberPosReverse[num])
            x, y = pos[0] + move_input[0], pos[1] + move_input[1]
            pos[0] = [x if 1 <= x <= 4 else pos[0]][0]
            pos[1] = [y if 1 <= y <= 4 else pos[1]][0]
            number = number_pos['{}'.format(pos)]
            oldNumberScore = newScoreList[num]
            nextNumberScore = newScoreList[number]
            syn = list(map(lambda x, y: abs(x) * abs(y), move_input, pos))
            # 0值移动
            if nextNumberScore == 0:
                newScoreList[number] = oldNumberScore
                newScoreList[num] = 0
            # 无法移动
            elif num == number:
                pass
            # 合并移动
            elif oldNumberScore == nextNumberScore and num != number:
                newScoreList[number] = 2 * oldNumberScore
                newScoreList[num] = 0
            # 边界移动
            elif oldNumberScore != nextNumberScore and 1 in syn or 4 not in syn:
                pass
            # 非边界移动
            elif oldNumberScore != nextNumberScore and 1 not in syn and 4 not in syn:
                x, y = pos[0] + move_input[0], pos[1] + move_input[1]
                next2NumberScore = newScoreList[number_pos['{}'.format([x, y])]]
                if next2NumberScore != nextNumberScore:
                    pass
                elif next2NumberScore == nextNumberScore:
                    newScoreList[number_pos['{}'.format([x, y])]] = 2 * next2NumberScore
                    newScoreList[number] = oldNumberScore
                    newScoreList[num] = 0

    return newScoreList


# 键盘控制函数
def keyboard_ctrl(event):
    move_output = [0, 0]
    if event.key == py.K_UP:
        move_output = [-1, 0]
    elif event.key == py.K_DOWN:
        move_output = [1, 0]
    elif event.key == py.K_RIGHT:
        move_output = [0, 1]
    elif event.key == py.K_LEFT:
        move_output = [0, -1]

    return move_output



# 随机得分生成
def random_score(score_list):
    values = list(score_list.values())
    pro = [2] * (2 + values.count(2)) + [4] * (1 + values.count(4))  # 以当前分数图中2或4出现的频率为概率
    blank = [[i if score_list[i] == 0 else 0][0] for i in range(1, 17)]
    blank = list(set(blank))
    blank.remove(0)
    if not blank:
        return 'GameOver'  # 游戏结束
    else:
        score_list[random.choice(blank)] = random.choice(pro)
        return score_list

# 统计并记录当前得分
def record_score(score_list, background):
    totalScore = 0
    values = list(score_list.values())
    for i in values: totalScore += i
    scoreSurf = BasicFont01.render('得分：{}'.format(totalScore), True, (0, 0, 0))
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (math.floor(0.1 * screen.get_width()), math.floor(0.05 * screen.get_height()))
    scoreRect.width = math.floor((rate - 0.15) / 2 * screen.get_width())
    scoreRect.height = math.floor((1 - rate2) / 3 * 2 * screen.get_height())
    py.draw.rect(screen, background, [scoreRect.topleft[0], scoreRect.topleft[1], scoreRect.width, scoreRect.height], 0)
    screen.blit(scoreSurf, scoreRect)
    return totalScore



# 启动界面

# 游戏结束
def game_over(score,bg):
    ip = '127.0.0.1'
    password = None
    #r = redis.Redis(host=ip, password=password, port=6379, db=2, decode_responses=True)
    #r.hset('2048','{}'.format(time.localtime()),score)
    py.draw.rect(screen,bg,[0,0,screen.get_width(),screen.get_height()],0)
    BasicFont02 = py.font.SysFont('/素材/simkai.ttf', 40)
    overSurf = BasicFont01.render('Game Over', True, (0, 0, 0))
    overRect = overSurf.get_rect()
    overRect.center = (math.floor(screen.get_width() / 2), math.floor(screen.get_height() / 2))
    scoreSurf = BasicFont02.render('最终得分:', True, (0, 0, 0))
    scoreRect = scoreSurf.get_rect()
    scoreRect.center = (math.floor(screen.get_width() / 2), math.floor(screen.get_height() * 0.6))
    numberSurf = BasicFont02.render('{}'.format(score), True, (0, 0, 0))
    numberRect = numberSurf.get_rect()
    numberRect.center = (math.floor(screen.get_width() / 2), math.floor(screen.get_height() * 0.7))
    time.sleep(3)
    sys.exit()


# 主程序
def game_start():
    global screen, rate
    py.init()
    clock = py.time.Clock()
    screen_x = 500  # 请调到合适的大小
    screen_y = math.ceil(screen_x * rate / rate2)
    screen = py.display.set_mode((screen_x, screen_y), depth=32)
    py.display.set_caption("终极2048")
    BackGround = [251, 248, 239]  # 灰色
    Icon = py.image.load('./素材/icon.png').convert_alpha()
    py.display.set_icon(Icon)
    screen.fill(color=BackGround)
    # 主界面下设计
    width = math.floor(screen_x * rate)
    bgSecond = py.image.load('./素材/BG_02.png').convert_alpha()
    bgSecond = py.transform.smoothscale(bgSecond, (width, width))
    bgSecondRect = bgSecond.get_rect()
    bgSecondRect.topleft = math.floor(screen_x * (1 - rate) / 2), math.floor(screen_y * (1 - rate2))

    # 主界面上部分设计

    # 预加载数据
    # draw_best(BackGround)
    posList = image_pos_list(bgSecondRect)
    imageList = pre_load_image(bgSecondRect)
    scoreList = dict(zip(list(range(1, 17)), [0] * 15 + [2]))  # 分数表
    numberPos = pre_move()
    scoreList = random_score(scoreList)
    totalScore=0
    # 主循环
    while True:
        screen.blit(bgSecond, bgSecondRect)  # 刷新屏幕
        if scoreList == 'GameOver':
            game_over(totalScore,BackGround)
        draw_image(scoreList, imageList, posList)  # 绘制得分
        totalScore = record_score(scoreList, BackGround)
        key = py.key.get_pressed()
        if key[py.K_ESCAPE]: exit()
        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit()
            elif event.type == py.KEYDOWN:
                move_input = keyboard_ctrl(event)  # 按下按键
                scoreList = number_move(numberPos, move_input, scoreList)  # 移动数字
                scoreList = random_score(scoreList)  # 在按下按键后生成新的数字

        py.display.update()
        clock.tick(FPS)


# 初始化 Pygame
py.init()
width, height = 500, 500
screen = py.Surface((width, height))


# Streamlit 应用程序
def main():
    st.title("Pygame in Streamlit")

    # 创建一个空的图像显示区域
    game_output = st.empty()

    # 运行游戏逻辑
    game_start()

    # 将 Pygame 屏幕转换为图像
    game_array = py.surfarray.array3d(screen)

    # 显示游戏图像
    game_output.image(game_array, channels="RGB")


if __name__ == '__main__':
    BasicFont01 = py.font.Font('./素材/simkai.ttf', 30)
    screen = py.display.set_mode((500, 500))
    rate = 0.95  # 游戏主界面下的宽度占整个游戏界面宽度的比例
    rate2 = 0.7  # 游戏主界面下的高度占整个游戏界面高度的比例
    internalWidth = 0.1  # 间隙比例
    FPS = 50  # 游戏帧率
    main()
