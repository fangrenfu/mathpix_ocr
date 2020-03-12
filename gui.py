# -*- coding: utf-8 -*-
# 窗口美化通用函数
import tkinter as tk
from tkinter import ttk

# 给某个窗口设置宽度和高度并且置中
def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)
    root.geometry(size)


# 一个顶层的进度条
class GressBar():
    def start(self):
        top = tk.Toplevel()
        self.master = top
        top.overrideredirect(True)
        top.title("进度条")
        tk.Label(top, text="发送请求识别中,请稍等……", fg="green").pack(pady=2)
        prog = ttk.Progressbar(top, mode='indeterminate', length=200)
        prog.pack(pady=10, padx=35)
        prog.start()

        top.resizable(False, False)
        top.update()
        curWidth = top.winfo_width()
        curHeight = top.winfo_height()
        scnWidth, scnHeight = top.maxsize()
        tmpcnf = '+%d+%d' % ((scnWidth - curWidth) / 2, (scnHeight - curHeight) / 2)
        top.geometry(tmpcnf)
        top.mainloop()

    def quit(self):
        if self.master:
            self.master.destroy()