import tkinter
import tkinter.messagebox


class Initor:  # 游戏初始化窗口类
    def __init__(self):
        # 游戏相关属性
        self.config = None
        # GUI控件属性
        self.window = tkinter.Tk()
        self.window.title('扫雷')
        self.window.resizable(False, False)
        self.window.geometry(self._set_center())
        self.window.iconbitmap('image/bomb.ico')

        self.frame1 = tkinter.Frame(self.window)
        self.frame1.pack(pady=10)
        self.frame2 = tkinter.Frame(self.window)
        self.frame2.pack()
        self.frame3 = tkinter.Frame(self.window)
        self.frame3.pack()
        self.frame4 = tkinter.Frame(self.window)
        self.frame4.pack()
        self.frame5 = tkinter.Frame(self.window)
        self.frame5.pack(pady=10)

        self.r_value = tkinter.IntVar()  # 单选框锚定值
        tkinter.Radiobutton(self.frame1, text='初级', variable=self.r_value, value=1,
                            command=self._set_disable).pack()  # 单选框
        rbtn = tkinter.Radiobutton(self.frame1, text='中级', variable=self.r_value, value=2, command=self._set_disable)
        rbtn.pack()
        rbtn.select()
        tkinter.Radiobutton(self.frame1, text='高级', variable=self.r_value, value=3, command=self._set_disable).pack()

        tkinter.Radiobutton(self.frame1, text='自定义', variable=self.r_value, value=4, command=self._set_normal).pack()
        tkinter.Label(self.frame2, text='行数：').pack(side=tkinter.LEFT)
        self.ent_r = tkinter.Entry(self.frame2, width=5)
        self.ent_r.pack()
        tkinter.Label(self.frame3, text='列数：').pack(side=tkinter.LEFT)
        self.ent_c = tkinter.Entry(self.frame3, width=5)
        self.ent_c.pack()
        tkinter.Label(self.frame4, text='地雷数：').pack(side=tkinter.LEFT)
        self.ent_num = tkinter.Entry(self.frame4, width=5)
        self.ent_num.pack()
        self._set_disable()

        btn = tkinter.Button(self.frame5, text="开始", font=('黑体', 16, 'bold'), command=self.click_start)
        btn.pack()
        tkinter.Label(self.frame5, justify='left', text="Tips：\n - 左键点开未知方格\n - 右键单击一次标记、单击二次自定义标记\n"
                                                        " - 标记后在数字方格位置单击滚轮排雷\n"
                                                        "注：排雷仅当标记个数与数字大小相等时有效，当周\n围无隐藏地雷时可直接单击滚轮以显示周围区域",
                      relief="groove").pack(pady=10)

        self.window.mainloop()

    def _set_disable(self):
        self.ent_c.config(state='disabled')
        self.ent_r.config(state='disabled')
        self.ent_num.config(state='disabled')

    def _set_normal(self):
        self.ent_c.config(state='normal')
        self.ent_r.config(state='normal')
        self.ent_num.config(state='normal')

    def click_start(self):  # 按下开始按钮，默认进入中级模式
        if self.r_value.get() == 0:
            self.config = None
        elif self.r_value.get() == 1:
            self.window.destroy()
            self.config = (9, 9, 10)
        elif self.r_value.get() == 2:
            self.window.destroy()
            self.config = (16, 16, 40)
        elif self.r_value.get() == 3:
            self.window.destroy()
            self.config = (16, 30, 99)
        elif self.r_value.get() == 4:
            if self.get_value():
                self.config = self.get_value()
                self.window.destroy()

    def get_value(self):
        r = self.ent_r.get()
        c = self.ent_c.get()
        num = self.ent_num.get()
        if r.isdigit() and int(r) >= 3 and c.isdigit() and int(c) >= 3 and num.isdigit() and int(num) <= int(r) * int(
                c):
            return int(r), int(c), int(num)
        else:
            tkinter.messagebox.showwarning(title="扫雷", message="行列数>=3,地雷数<=行*列!")
            return None

    def _set_center(self):
        w = 320
        h = 380
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        x = (sw - w) / 2
        y = (sh - h) / 2
        return f"{w}x{h}+{int(x)}+{int(y)}"


# i = Initor()
# print(i.config)
# del i
