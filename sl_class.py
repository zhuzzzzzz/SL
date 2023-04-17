from map_class import *
from game_initor import *
from map_func import _check_value


class SL:  # 游戏地图交互类
    def __init__(self, r, c, num):
        # 游戏参数
        self.r = r
        self.c = c
        self.game_map = Map(r, c, num)  # 生成地图对象
        self.run_flag = True
        self.seconds = 0
        self.restart_flag = False

        # 图形化程序
        # 图形参数
        self.window = tkinter.Tk()
        self.window.geometry('+-1500+-2000')
        self.window.title('扫雷')
        self.window.resizable(False, False)
        self.window.iconbitmap('image/bomb.ico')
        self.image_bomb = tkinter.PhotoImage(file='image/bomb.png')
        self.image_invisible = tkinter.PhotoImage(file='image/invisible.png')
        self.image_nothing = tkinter.PhotoImage(file='image/nothing.png')
        self.image_flag = tkinter.PhotoImage(file='image/flag.png')
        self.image_ask = tkinter.PhotoImage(file='image/ask.png')
        self.image_error = tkinter.PhotoImage(file='image/error.png')
        self.image = []
        for i in range(1, 9):
            self.image.append(tkinter.PhotoImage(file=f"image/{i}.png"))

        # 图形对象
        self.frame1 = tkinter.Frame(self.window, pady=5)
        self.frame2 = tkinter.Frame(self.window)
        self.frame1.grid()
        self.frame2.grid()

        self.counter = tkinter.Label(self.frame1, relief='groove')
        self.timer = tkinter.Label(self.frame1, relief='groove')
        self.timer.grid(row=0, column=0, padx=10)
        self.counter.grid(row=0, column=1, padx=10)

        self.lbls = []  # 生成标签矩阵
        for i in range(0, r):
            self.lbls.append([])
            for j in range(0, c):
                self.lbls[i].append(
                    tkinter.Label(self.frame2, height=30, width=30, image=self.image_invisible, relief=tkinter.RAISED))
                self.lbls[i][j].grid(row=i, column=j)
                self.lbls[i][j].bind('<Button>', self.click_handle)
                # self.lbls[i][j].bind('<Double-Button>', self.click_handle)

        self.update_counter(self.game_map.bomb_left)
        self.update_timer()
        self._set_center()  # 这行一定要放在定时器和计数器的后面，因为这两个对象也有大小，放前面会出现显示不全的问题
        self.window.mainloop()

    def set_image(self, r, c, value):  # 设置Lable标签上显示的图片
        if value == -1:
            self.lbls[r][c].config(image=self.image_bomb, relief=tkinter.SUNKEN)
        elif value == 0:
            self.lbls[r][c].config(image=self.image_nothing, relief=tkinter.SUNKEN)
        else:
            self.lbls[r][c].config(image=self.image[value - 1], relief=tkinter.SUNKEN)

    def click_handle(self, event):
        if self.run_flag:
            res = self._name_get_r_c(event.widget)
            r = res[0]
            c = res[1]
            if event.num == 1:  # 左键单击
                if _check_value(self.game_map.disp_ctrl_map, r, c) == 0:  # 只有单击未显示的方格才有效，防止出现点击排除后的地雷显示失败的bug
                    if not self._left_click(self.game_map.explore_map(r, c)):
                        self.run_flag = False
                        tkinter.messagebox.showwarning(title="扫雷", message="失败!")
                        self.if_restart()
            elif event.num == 2:  # 滚轮单击
                self._mid_click(r, c)
            elif event.num == 3:  # 右键单击
                self._right_click(self.game_map.mark_map(r, c))
        if self.run_flag and self.game_map.is_clear():  # 当游戏仍在进行且地图被清空。防止在10*10、99雷的极端情况下出现点一次地图后提示成功的bug
            self.run_flag = False
            tkinter.messagebox.showinfo(title="扫雷", message="成功!")
            self.if_restart()

    def _left_click(self, obj):
        for item in obj:  # 首先让单击位置可见
            self.set_image(item[1], item[2], item[3])
        if obj.pop()[0]:  # 判断是否踩雷
            return True
        else:
            return False

    def _right_click(self, obj):
        if obj:
            if obj[2] == 0:
                self.lbls[obj[0]][obj[1]].config(image=self.image_invisible)
            elif obj[2] == 1:
                self.lbls[obj[0]][obj[1]].config(image=self.image_flag)
            elif obj[2] == 2:
                self.lbls[obj[0]][obj[1]].config(image=self.image_ask)

    def _mid_click(self, r, c):
        res = self.game_map.clear_mine(r, c)
        if res:
            for item in res:
                if not item[0]:
                    self.lbls[item[1]][item[2]].config(image=self.image_error, relief=tkinter.SUNKEN)  # 显示标错的方块
                else:
                    self.set_image(item[1], item[2], item[3])  # 根据值显示其他方块
            for item in res:
                if not item[0]:
                    self.run_flag = False
                    tkinter.messagebox.showwarning(title="扫雷", message="失败!")
                    self.if_restart()
                    break
            self.update_counter(self.game_map.bomb_left)

    def _name_get_r_c(self, obj):  # 传递Label标签对象获取其在矩阵中所处的位置
        if obj._name.lstrip('!label'):
            num = int(obj._name.lstrip('!label'))
        else:  # 考虑到特殊情况
            num = 1
        r = (num - 1) // self.c
        c = num % self.c
        if c == 0:  # 考虑到特殊情况，最后一个余数为0，则赋列数值
            c = self.c
        return r, c - 1

    def update_counter(self, value):
        value = str(value)
        if len(value) <= 1:
            self.counter.config(height=1, width=2, text=value, font=('微软雅黑', 20, 'bold'))
        else:
            self.counter.config(height=1, width=len(value), text=value, font=('微软雅黑', 20, 'bold'))

    def update_timer(self):
        value = str(self.seconds)
        if len(value) <= 1:
            self.timer.config(height=1, width=2, text=value, font=('微软雅黑', 20, 'bold'))
        else:
            self.timer.config(height=1, width=len(value), text=value, font=('微软雅黑', 20, 'bold'))
        self.seconds += 1
        if self.run_flag:
            self.timer.after(1000, self.update_timer)

    def _set_center(self):
        self.window.update()
        w = self.window.winfo_width()
        h = self.window.winfo_height()
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.window.geometry(f"{w}x{h}+{int(x)}+{int(y)}")

    def if_restart(self):
        if tkinter.messagebox.askquestion(title="扫雷", message="是否重新开始？") == 'yes':
            self.window.destroy()
            self.restart_flag = True
            return True
        else:
            return False
            # self.window.quit()

# c = SL(3, 3, 1)
