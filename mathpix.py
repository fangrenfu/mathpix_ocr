import json
import os
from collections import OrderedDict
import base64
from urllib import parse
from PIL import Image, ImageTk
import requests
import sys
import pyperclip
import datetime


# 基本函数
# common function

# 从config.json中读取配置文件
# read app setting from config.json
def get_config():
    config_file_name = 'config.json'
    global config
    if os.path.isfile(config_file_name):
        with open(config_file_name) as config_file:
            config = json.load(config_file, object_pairs_hook=OrderedDict)
    else:
        print('config.json lost!')
    return config


# 保存配置
def save_config(app_id, app_key):
    print('save done!')


# 从剪贴板中返回base64的图像编码
def get_image_base64_from_clipboard():
    if sys.platform.startswith('linux'):
        # Linux获得剪贴板中图片的地址，去掉前面file://部分 "/home/kiee/图片/Screenshot_20200310_120948.png"
        filename = pyperclip.paste()[7:]
        filename = parse.unquote(filename)
    else:
        # Window和Mac中使用ImageGrab获取图像并保存
        from PIL import ImageGrab
        im = ImageGrab.grabclipboard()
        # 生成一个根据时间的字符串，用于临时保存图片
        filename = '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now()) + '.png'
        im.save(filename, 'PNG')
    image_data = open(filename, "rb").read()
    return "data:image/jpg;base64," + base64.b64encode(image_data).decode()


# Mathpix service with the given arguments, headers, and timeout.
# 以给定参数调用Mathpix服务接口
def latex(args,app_info, timeout=30):
    headers = {
        # 调用的APP_ID和APP_KEY,账户注册后可以查看到。写在config.json文件中
        'app_id': app_info['app_id'],
        'app_key': app_info['app_key'],
        'Content-type': 'application/json'
    }
    service = 'https://api.mathpix.com/v3/latex'
    r = requests.post(service,
                      data=json.dumps(args), headers=headers, timeout=timeout)
    return json.loads(r.text)

#  缩放图像filename到指定大小,保持纵横比，返回改变大小后的图片
def image_resize(filename, width, height):
    '''
    resize a pil_image object so it will fit into
    a box of size w_box times h_box, but retain aspect ratio
    对一个pil_image对象进行缩放，让它在一个矩形框内，还能保持比例
    '''
    pil_image = Image.open(filename)
    w, h = pil_image.size
    f1 = 1.0 * width / w  # 1.0 forces float division in Python2
    f2 = 1.0 * height / h
    factor = min([f1, f2])
    # print(f1, f2, factor) # test
    # use best down-sizing filter
    width = int(w * factor)
    height = int(h * factor)
    return pil_image.resize((width, height), Image.ANTIALIAS)
