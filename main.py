# -*- coding: utf-8 -*-
import time

import gui
from mathpix import *
import tkinter as tk
from PIL import ImageTk
from shutil import copyfile
import tkinter.messagebox
import tkinter.filedialog


# 定义主窗口类
# define main windows class
class MainWin():
    # 用于动态生成各种格式返回的空间
    bt_formats = dict()
    en_formats = dict()
    lb_formats = dict()

    # 初始化界面
    # init interface
    def __init__(self):
        self.filename = 'latex.png'
        self.win = tk.Tk()
        # 顶部工具栏
        self.bt_file = tk.Button(text='打开文件', height=1, command=self.file)
        self.bt_file.grid(row=0, column=0, pady=10, padx=5)

        self.bt_paste = tk.Button(text='从剪贴板载入', height=1, command=self.clipboard)
        self.bt_paste.grid(row=0, column=1)

        self.bt_mathpix = tk.Button(text='用Mathpix ORC识别', height=1, command=self.get_mathpix)
        self.bt_mathpix.grid(row=0, column=2, padx=5, columnspan=2)

        self.lb_space = tk.Label(text="待识别图像", width=10, height=7)
        self.lb_space.grid(row=1, column=0, columnspan=4)
        self.lb_image = tk.Label()
        # 从config.json中读取类型设置
        # read formats from config.json
        # self.format_setting = ['latex_normal', 'latex_styled', 'latex_simplified', 'latex_list', 'asciimath']
        self.format_setting = get_config()['formats']
        # 生成用于放置返回结果的文本框和按钮
        format_start = 2
        current_index = 0
        for format in self.format_setting:
            self.build_format_row(format, format_start, current_index)
            current_index = current_index + 1

        # 设置窗口属性，并将其放置到中间
        self.win.update()
        self.win.title('Mathpix OCR 接口使用')
        self.win.resizable(width=False, height=False)
        gui.center_window(self.win, self.win.winfo_width(), self.win.winfo_height())
        tk.mainloop()

    # 动态生成用于放置返回结果的文本框和按钮
    # Dynamically generate label,entry and buttons for placing returned results
    def build_format_row(self, format, start, index):
        label_column = 0
        entry_columnspan = 2
        entry_column = 1
        entry_width = 45
        button_column = 3
        row_pady = 5
        self.lb_formats[format] = tk.Label(text=format + ':')
        self.lb_formats[format].grid(row=start + index, column=label_column, pady=row_pady, sticky=tk.E, padx=10)
        self.en_formats[format] = tk.Entry(width=entry_width)
        self.en_formats[format].grid(row=start + index, column=entry_column, columnspan=entry_columnspan)
        self.bt_formats[format] = tk.Button(text='复制', height=1, width=10,
                                            command=(lambda: self.copy(self.en_formats[format])))
        self.bt_formats[format].grid(row=start + index, column=button_column, padx=10)

    # Common module for calling Mathpix OCR service from Python.
    # 使用Python调用Mathpix OCR接口通用模块
    def get_mathpix(self):
        try:
            global latex_simple
            #  计算时间
            start = time.time()
            # image_base64 = get_image_base64_from_clipboard()
            # 文件已经准备好了，直接从临时文件中获取
            image_data = open(self.filename, "rb").read()
            image_base64 = "data:image/jpg;base64," + base64.b64encode(image_data).decode()
            app_info = get_config()
            r = latex({'src': image_base64, 'formats': self.format_setting}, app_info)
            print(json.dumps(r, indent=4, sort_keys=True))
            for f in self.format_setting:
                self.en_formats[f].delete(0, tk.END)
                self.en_formats[f].insert(0, r[f])
            end = time.time()
            last_time = ('（耗时' + format(end - start, '0.3f') + '秒）')
            self.win.title('Mathpix OCR 接口使用' + last_time)
            return r
        except ConnectionError:
            tk.messagebox.showerror('错误', '连接错误或超时！', )
    # 将内容复制到剪贴板
    # copy content to clipboard
    def copy(self, entry):
        pyperclip.copy(entry.get())
        entry.select_from(0)

    # 从剪贴板获取图像
    # get image from clipborad
    def clipboard(self):
        # self.filename = './temp/{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now()) + '.png'
        try:
            self.filename = 'latex.png'
            if sys.platform.startswith('linux'):
                # Linux获得剪贴板中图片的地址，去掉前面file://部分 "/home/kiee/图片/Screenshot_20200310_120948.png"
                file_temp = pyperclip.paste()[7:]
                file_temp = parse.unquote(file_temp)
                # 拷贝文件到当前目录
                copyfile(file_temp, self.filename)
            else:
                # windows系统下先尝试抓取剪贴板内容
                from PIL import ImageGrab
                # Window和Mac中使用ImageGrab获取图像并保存
                im = ImageGrab.grabclipboard()
                # 生成一个根据时间的字符串，用于临时保存图片
                im.save(self.filename, 'PNG')
            self.load_image()
        except(IOError,AttributeError):
            tk.messagebox.showwarning('错误', '请先复制图片到剪贴板')
    # 根据设置图像的大小进行界面中展示
    def load_image(self):
        # 待识别图像缩放后大小
        print(self.filename)
        width = self.win.winfo_width() - 10
        height = 100
        pil_image_resized = image_resize(self.filename, width, height)
        tk_image = ImageTk.PhotoImage(pil_image_resized)
        # tk_image = ImageTk.PhotoImage(file=self.filename)
        self.lb_image.destroy()
        self.lb_image = tk.Label(text="abc", image=tk_image)
        self.lb_image.grid(row=1, column=0, columnspan=4)
        tk.mainloop()

    # 从文件载入
    def file(self):
        filename = tk.filedialog.askopenfile()
        if filename is not None:
            self.filename = filename.name
            self.load_image()


if __name__ == '__main__':
    MainWin()
