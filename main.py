# 导入库
import os
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from PIL import  ImageTk
import db_handler

#初始化历史战绩
mark = [3,3,3,6,5,6,3,16,10,11,12,14]

#写记录
def write_record(mark):
    f = open('records.txt', 'w')
    s = f.write(str(mark))
    f.close()
#读记录
def read_record(mark):
    try:
        f = open('records.txt', 'r')
    except:
        f = open('records.txt', 'w+')
    mark = f.read()
    mark = eval(mark)
    f.close()
    return mark   
# 注册界面
def register():
    # 创建topLevel,设置窗口大小，位置，标题，背景
    register_top = tk.Toplevel(root)
    register_top.geometry('300x160+200+200')
    register_top.title('注册')
    register_top['bg'] = '#3c3836'
    register_top.resizable(0,0)

    # 将注册名字，密码，确认密码设置成全局变量
    global new_name, new_pwd, new_pwd_confirm

    # 用户名
    new_name = tk.StringVar()
    tk.Label(register_top, text='用户名：', bg='#3c3836',
             fg='white',).place(x=10, y=20)
    entry_new_name = tk.Entry(register_top, textvariable=new_name,
                              bg='#3c3836', fg='#c6c6c6')
    entry_new_name.place(x=130, y=10)

    # 密码
    new_pwd = tk.StringVar()
    tk.Label(register_top, text='密码：', bg='#3c3836',
             fg='white', ).place(x=10, y=50)
    entry_new_pwd = tk.Entry(register_top, textvariable=new_pwd,
                              bg='#3c3836', fg='#c6c6c6', show='*')
    entry_new_pwd.place(x=130, y=50)

    # 确认密码
    new_pwd_confirm= tk.StringVar()
    tk.Label(register_top, text='确认密码：', bg='#3c3836',
             fg='white', ).place(x=10, y=90)
    entry_new_pwd_confirm = tk.Entry(register_top, textvariable=new_pwd_confirm,
                             bg='#3c3836', fg='#c6c6c6', show='*')
    entry_new_pwd_confirm.place(x=130, y=90)

    # 确认按钮
    btn_confirm = tk.Button(register_top, text='确定', bg='#3c3836', fg='white',
                            activebackground='#3c3836', command=confirm)
    btn_confirm.place(x=250, y=120)


# 注册检测
def confirm():
    # 获取注册用户名和密码
    username = new_name.get().strip()
    pwd = new_pwd.get().strip()
    pwd_confirm = new_pwd_confirm.get().strip()

    # 检测两次密码是否相同
    if not pwd == pwd_confirm:
        messagebox.showwarning('警告', '两次密码不一致')
    else:
        # 调用
        res, msg = db_handler.register(username, pwd)
        if res:
            messagebox.showinfo('信息', msg)
        else:
            messagebox.showwarning('警告', msg)


# 登录检测
def login():
    # 获取输入的用户名和密码
    username = user_name.get().strip()
    pwd = pwd_name.get().strip()
    #
    res, msg = db_handler.check(username, pwd)
    if res:
        # 登录成功，设置登录用户， 销毁登录界面，调用信息界面
        global LOGIN_USER
        LOGIN_USER = username
        root.destroy()
        information()
    else:
        messagebox.showwarning('警告', msg)


# 个人信息界面
def information():
    # 将窗口、用户字典、头像设置成全局变量
    global window, user_dic, head_pic
    # 设置信息框大小，位置，标题
    width = 600
    height = 500
    align_str = '%dx%d+%d+%d'%(width, height, (screen_width-width)//2, (screen_height-height)//2)
    window = tk.Tk()
    window.geometry(align_str)
    window.title('个人信息')
    window.resizable(0,0)

    # 获取登录成功的用户字典，得到数据
    user_dic = db_handler.return_user_dic(LOGIN_USER)
    # 头像
    head_pic = ImageTk.PhotoImage(file=user_dic['image'][0])
    head_label = tk.Label(window, image=head_pic, justify='center')
    head_label.place(x=user_dic['image'][1], y=user_dic['image'][2])
    head_text = tk.Label(window, text='头像', font=('黑体', 15))
    head_text.place(x=210, y=50)
    # 选择按钮
    chooseBtn = tk.Button(window, text='选择', fg='black',width=10,
                          font=('黑体',15), command=selectPhoto)
    chooseBtn.place(x=180, y=100)
    # 性别：单选
    sex_text = tk.Label(window, text='性别：', font=('黑体', 15))
    sex_text.place(x=0, y=190)
    var = tk.StringVar()
    var.set(user_dic['sex'])
    female_btn = tk.Radiobutton(window, font=('黑体', 15), value='女',
                                text='女', variable=var)
    female_btn.place(x=30, y=230)
    male_btn = tk.Radiobutton(window, font=('黑体', 15), value='男',
                                text='男', variable=var)
    male_btn.place(x=150, y=230)

    # 爱好：多选
    hobby_text = tk.Label(window, text='爱好:', font=('黑体', 15))
    hobby_text.place(x=0, y=270)

    checkVar1 = tk.IntVar()
    checkVar2 = tk.IntVar()
    checkVar3 = tk.IntVar()
    checkVar4= tk.IntVar()
    c1 = tk.Checkbutton(window, text='电影', variable=checkVar1,
                        onvalue=1, offvalue=0, font=('黑体',15))
    c2 = tk.Checkbutton(window, text='音乐', variable=checkVar2,
                        onvalue=1, offvalue=0, font=('黑体', 15))
    c3 = tk.Checkbutton(window, text='看书', variable=checkVar3,
                        onvalue=1, offvalue=0, font=('黑体', 15))
    c4 = tk.Checkbutton(window, text='其他', variable=checkVar4,
                        onvalue=1, offvalue=0, font=('黑体', 15))
    c1.place(x=30, y=310)
    c2.place(x=150, y=310)
    c3.place(x=30, y=350)
    c4.place(x=150, y=350)

    if user_dic['hobby'][0]:
        c1.select()
    if user_dic['hobby'][1]:
        c2.select()
    if user_dic['hobby'][2]:
        c3.select()
    if user_dic['hobby'][3]:
        c4.select()

    # 地区
    area_text = tk.Label(window, text='地区：', font=('黑体', 15))
    area_text.place(x=0, y=390)
    cmb = ttk.Combobox(window, font=('黑体', 15))
    cmb.place(x=30, y= 430)
    # 设置value值
    cmb['value'] = ['北京市','天津市','上海市','重庆市','河北省','山西省','辽宁省',
                    '吉林省','黑龙江省','江苏省','浙江省','安徽省','福建省','江西省',
                    '山东省','河南省','湖北省','湖南省','广东省','海南省','四川省',
                    '贵州省','云南省','陕西省','甘肃省','青海省','台湾省','港澳地区','其他']
    cmb.set(user_dic['area'])

    # 右半边布局
    btn_bg = tk.Label(window, bg='#3c3836', width=300, height=500)
    btn_bg.place(x=300, y=0)

    def game():

        user_dic['sex'] = var.get()
        user_dic['hobby'][0] = checkVar1.get()
        user_dic['hobby'][1] = checkVar2.get()
        user_dic['hobby'][2] = checkVar3.get()
        user_dic['hobby'][3] = checkVar4.get()
        user_dic['area'] = cmb.get()
        # 保存修改后的数据
        db_handler.save(user_dic, LOGIN_USER)
        window.destroy()
        import pygame  # 引入模块
        import sys

        class Bird(object):  # 定义鸟类
            def __init__(self):  # 定义初始化方法
                self.birdRect = pygame.Rect(65, 50, 48, 48)  # 定义鸟的矩形框
                self.birdStatus = [pygame.image.load("1.png"), pygame.image.load("2.png"),
                                   pygame.image.load("dead.png")]  # 定义鸟状态的列表
                self.status = 0  # 默认状态为飞行
                self.birdX = 120  # 定义鸟坐标位置
                self.birdY = 350
                self.jump = False  # 默认鸟自由下落
                self.jumpSpeed = 20
                self.gravity = 5
                self.dead = False  # 默认鸟活着

            def birdUpdate(self):  # 定义小鸟飞行函数
                if self.jump:  # 小鸟上升
                    self.jumpSpeed -= 0.8
                    self.birdY -= self.jumpSpeed
                else:  # 小鸟下落
                    self.gravity += 0.2
                    self.birdY += self.gravity
                self.birdRect[1] = self.birdY

        class Pipeline(object):  # 定义管道类
            def __init__(self):
                self.wallx = 400  # 定义坐标
                self.pineUp = pygame.image.load("top.png")  # 加载图片
                self.pineDown = pygame.image.load("bottom.png")

            def updatePipeline(self):
                self.wallx -= 5  # 设定管道移动
                if self.wallx < 50:  # 积分规则
                    global score
                    score += 1
                    self.wallx = 400  # 更新管道位置

        def creatMap1():
            '''
             协助制作开始界面，为creatMap函数绘制出图的首界面
            '''
            screen.fill((255, 255, 255))
            screen.blit(background, (0, 0))
            screen.blit(Pipeline.pineUp, (Pipeline.wallx, -100))
            screen.blit(Pipeline.pineDown, (Pipeline.wallx, 400))
            screen.blit(Bird.birdStatus[Bird.status], (120, 350))
            screen.blit(font.render(str(score), -1, (255, 255, 255)), (200, 50))
            pygame.display.update()

        def creatMap():  # 绘制地图
            screen.fill((255, 255, 255))
            screen.blit(background, (0, 0))
            screen.blit(Pipeline.pineUp, (Pipeline.wallx, -100))  # 管道坐标位置
            screen.blit(Pipeline.pineDown, (Pipeline.wallx, 400))
            Pipeline.updatePipeline()

            if Bird.dead:
                Bird.status = 2  # 列表里鸟阵亡后的照片
            elif Bird.jump:
                Bird.status = 1  # 列表里鸟飞行的照片
            screen.blit(Bird.birdStatus[Bird.status], (Bird.birdX, Bird.birdY))  # 鸟的坐标位置
            Bird.birdUpdate()

            screen.blit(font.render(str(score), -1, (255, 255, 255)), (200, 50))  # 设置文字的颜色及坐标位置
            pygame.display.update()

        def checkDead():  # 检查鸟是否阵亡
            upRect = pygame.Rect(Pipeline.wallx, -100,
                                 Pipeline.pineUp.get_width(),
                                 Pipeline.pineUp.get_height())  # 管道的矩形位置
            downRect = pygame.Rect(Pipeline.wallx, 410,
                                   Pipeline.pineDown.get_width(),
                                   Pipeline.pineDown.get_height())
            if upRect.colliderect(Bird.birdRect) or downRect.colliderect(Bird.birdRect):  # 检验鸟是否与上下管道相撞
                Bird.dead = True
            if not 0 < Bird.birdRect[1] < height:  # 检验鸟是否飞出屏幕范围，若飞出屏幕范围则认为鸟死亡
                Bird.dead = True
                return True
            else:
                return False

        def getResult():  # 游戏得分统计
            '''
            设置文字字体、颜色及显示位置
            '''
            final_text1 = "Game Over"
            final_text2 = "Your final score is: " + str(score)
            final_text3 = "Cheer up next time"
            ft1_font = pygame.font.SysFont("Arial", 70)
            ft1_surf = font.render(final_text1, 1, (242, 3, 36))
            ft2_font = pygame.font.SysFont("Arial", 50)
            ft2_surf = font.render(final_text2, 1, (0, 0, 255))
            ft3_font = pygame.font.SysFont("Arial", 30)
            ft3_surf = font.render(final_text3, 1, (255, 0, 255))
            screen.blit(ft1_surf, [screen.get_width() / 2 - ft1_surf.get_width() / 2, 100])
            screen.blit(ft2_surf, [screen.get_width() / 2 - ft2_surf.get_width() / 2, 200])
            screen.blit(ft3_surf, [screen.get_width() / 2 - ft3_surf.get_width() / 2, 300])
            pygame.display.flip()

        if 1:
            global score
            pygame.init()  # 初始化pygame
            pygame.display.set_caption("保护小鸟，冲冲冲！")  # 设置游戏名字
            pygame.font.init()  # 初始化字体
            font = pygame.font.SysFont(None, 50)  # 定义默认字体和大小
            size = width, height = 400, 720
            screen = pygame.display.set_mode(size)  # 定义屏幕大小
            clock = pygame.time.Clock()  # 设置时钟
            Pipeline = Pipeline()  # 确切类别中的对象
            Bird = Bird()
            score = 0  # 初始化得分
            vol_allow = 1  # 定义执行条件
            bg_music = "bg_music.ogg"
            die_wav = "die_music.wav"
            pygame.mixer.music.load(bg_music)
            die_sound = pygame.mixer.Sound(die_wav)
            pygame.mixer.music.play(-1, 0)  # 循环播放背景音乐

            running = True
            running2 = True
            '''
            两层循环，外层相当于设置了一个开始函数，按下任意键开始游戏，
            而内层则为程序的核心部分，体现了整个游戏进行的效果
            '''
            while running:
                for event2 in pygame.event.get():  # 轮询event2
                    if event2.type == pygame.QUIT:  # 判断是否为退出实践
                        running = False
                    background = pygame.image.load("background.png")  # 定义背景图
                    creatMap1()  # 创建游戏首界面
                    if event2.type == pygame.KEYDOWN or event2.type == pygame.MOUSEBUTTONDOWN:  # 按下任意键或点击鼠标开始游戏
                        while running2:
                            clock.tick(60)  # 每秒执行60次
                            for event in pygame.event.get():  # 轮询event
                                if event.type == pygame.QUIT:
                                    running2 = False
                                    running = False
                                if (
                                        event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not Bird.dead:  # 判断是否有键或鼠标被按下且鸟是否活着
                                    Bird.jump = True  # 鸟跳跃
                                    Bird.gravity = 5  # 鸟的重力
                                    Bird.jumpSpeed = 10  # 鸟的跳跃速度
                            background = pygame.image.load("background.png")
                            if checkDead():  # 判断鸟的生命状态
                                if vol_allow:  # 如果鸟死了则执行以下语句
                                    pygame.mixer.music.stop()  # 暂停背景音乐
                                    die_sound.play()  # 播放死亡音效
                                    vol_allow = 0  # 改变vol_allow的值轮询后不再反复播放死亡音效
                                getResult()  # 获得分数并输出结果
                            else:
                                creatMap()  # 创建地图

            pygame.quit()  # 卸载pygame模块
            mark.append(score)
        information()



    # 开始游戏按钮
    start_btn = tk.Button(window, bg='#3c3836', fg='white', text='开始游戏',
                          font=('黑体', 20), activebackground='#3c3836', command=game)
    start_btn.place(x=400, y=120)
    # 后10次历史战绩按钮
    history_btn = tk.Button(window, bg='#3c3836', fg='white', text='历史战绩',
                          font=('黑体', 20), activebackground='#3c3836',
                            command=lambda:db_handler.draw_fig(LOGIN_USER, mark))
    history_btn.place(x=400, y=220)
    # 退出游戏按钮
    esc_btn = tk.Button(window, bg='#3c3836', fg='white', text='退出游戏',
                          font=('黑体', 20), activebackground='#3c3836', command=escExit)
    esc_btn.place(x=400, y=320)

    window.mainloop()


# 选择图片
def selectPhoto():
    # 获取图片路径
    file = filedialog.askopenfilename(initialdir='C:/', title='选择一张照片')
    if len(file)>0:
        # 调用显示图片的方法
        resized, x_pos, y_pos, file = db_handler.show_photo(file,LOGIN_USER)
        global head_pic
        head_pic = ImageTk.PhotoImage(resized)
        head_label = tk.Label(window, image=head_pic)
        head_label.place(x=x_pos, y=y_pos)
    # 存储修改后的数据
    db_handler.save(user_dic, LOGIN_USER)
    window.mainloop()


# 退出游戏
def escExit():
    write_record(mark)
    window.destroy()

# 创建全局变量LOGIN_USER代表登录成功后的用户
LOGIN_USER = ''
# 获取文件所在的文件夹
BASE_PATH = os.path.dirname(__file__)
# 检测是否存在users_db，没有则创建，用来存储用户文件夹
if not os.path.exists(os.path.join(BASE_PATH, 'users_db')):
    os.mkdir(os.path.join(BASE_PATH, 'users_db'))


# 创建登录界面
mark = read_record(mark)
root = tk.Tk()
# 设置窗口标题、长、宽、位置、背景颜色
root.title('登录')
screen_width, screen_height = root.maxsize()
width, height = 600, 350
align_str = '%dx%d+%d+%d'%(width, height, (screen_width-width)//2, (screen_height-height)//2)
root.geometry(align_str)
root.resizable(0, 0)
root['bg'] = '#3c3836'

# 设置用户标签、用户输入框
user_lable = tk.Label(root, text='用户名:', font=('黑体', 20), width=10,
                      bg='#3c3836', fg='white')
user_lable.place(x=50, y=50)
user_name = tk.StringVar()
user_entry = tk.Entry(root, textvariable=user_name, font=('黑体', 20),
                      bg='#3c3836', fg='#c6c6c6')
user_entry.place(x=200, y=50)

# 设置密码标签、密码输入框
pwd_lable = tk.Label(root, text='密 码：', font=('黑体', 20), width=10,
                      bg='#3c3836', fg='white')
pwd_lable.place(x=50, y=150)
pwd_name = tk.StringVar()
pwd_entry = tk.Entry(root, textvariable=pwd_name, font=('黑体', 20),
                      bg='#3c3836', fg='#c6c6c6', show='*')
pwd_entry.place(x=200, y=150)

# 设置注册按钮，绑定方法为register:注册界面
register_btn = tk.Button(root, text='注册', font=('黑体', 20), width=10,
                         bg='#3c3836', fg='white', activebackground='#3c3836',
                         command=register)
register_btn.place(x=100, y=250)
# 设置登录按钮，绑定方法为login: 检测登录
login_btn = tk.Button(root, text='登录', font=('黑体', 20), width=10,
                         bg='#3c3836', fg='white', activebackground='#3c3836',
                         command=login)
login_btn.place(x=350, y=250)

root.mainloop()