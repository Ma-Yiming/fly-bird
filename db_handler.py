'''
用来处理数据
'''
# 导入库
import os
import json
import hashlib
from PIL import Image
import matplotlib.pyplot as plt

# 获取users_db的文件夹路径
USERS_PATH = os.path.join(os.path.dirname(__file__), 'users_db')


# 注册数据检测
def register(username, pwd):
    # 检测用户文件夹是否存在
    user_path = os.path.join(USERS_PATH, username)
    if os.path.exists(user_path):
        return False, '用户名已存在！'

    # 密码加密操作
    pwd = pwd_salt(pwd)
    # 用户数据字典{用户名， 密码， 头像路径， 位置， 性别， 爱好，地区，历史战绩，
    # 地区，开局分数}
    user_dic = {
        'username': username,
        'pwd': pwd,
        'image': [os.path.join(os.path.dirname(__file__), 'user.png'), 0, 0],
        'sex': '男',
        'hobby': [0, 0, 0, 0],
        'area': '',
        'score': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'point': 0,
    }

    # 创建用户文件夹，存储用户数据
    os.mkdir(os.path.join(USERS_PATH, username))
    save(user_dic, username)
    return True, f'用户{username}注册成功'


# 密码加密
def pwd_salt(pwd):
    md5_object = hashlib.md5()
    md5_object.update('左青龙，右白虎'.encode('utf-8'))
    md5_object.update(pwd.encode('utf-8'))
    md5_object.update('中间一只小老鼠'.encode('utf-8'))
    return  md5_object.hexdigest()


# 存储用户数据
def save(user_dic, username):
    user_path = os.path.join(USERS_PATH, username, f'{username}.json')
    with open(user_path, 'w', encoding='utf-8') as f:
        json.dump(user_dic, f, ensure_ascii=False)


# 登录数据检测
def check(username, pwd):
    user_path = os.path.join(USERS_PATH, username, f'{username}.json')
    # 密码加密
    pwd = pwd_salt(pwd)
    if os.path.exists(user_path):
        user_dic = return_user_dic(username)
        if user_dic['username'] == username and user_dic['pwd'] == pwd:
            return True, '登录成功'
        else:
            return False, '用户名或密码错误'
    else:
        return False, '用户名或密码错误'


# 返回用户字典
def return_user_dic(username):
    user_path = os.path.join(USERS_PATH, username, f'{username}.json')
    with open(user_path, 'r', encoding='utf-8') as f:
        user_dic = json.load(f)
    return user_dic


# 画图
def draw_fig(username, mark):
    user_dic = return_user_dic(username)
    x= range(1, 11)
    #y = user_dic['score'][:-11:-1]
    y = mark[-10:]
    # 绘图
    s = 'The highest mark: '+ str(max(mark))
    plt.title(s)
    plt.plot(x, y, lw=3, marker='*', ms=10  )
    plt.show()

# 显示图片
def show_photo(file, username):
    image = Image.open(file)
    w, h = image.size
    # 重置尺寸
    resized = resize(w, h, 170, 170, image)
    # 保存头像
    save_path = os.path.join(USERS_PATH, username, 'user.png')
    resized.save(save_path)
    w, h = resized.size
    x_pos, y_pos = (170-w)//2, (170-h)//2
    # 返回缩放的图片、位置、存储路径
    return resized, x_pos, y_pos, save_path


# 缩放图片
def resize(w, h, new_w, new_h, pil_image):
    f1 = 1.0 * new_w / w
    f2 = 1.0 * new_h / h
    # 以最小的比例缩放
    factor = min(f1, f2)
    width = int(w * factor)
    height = int(h * factor)
    return pil_image.resize((width, height), Image.ANTIALIAS)


