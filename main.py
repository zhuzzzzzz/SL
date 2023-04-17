from sl_class import *
from game_initor import *

run_flag = True
while run_flag:
    ini = Initor()  # 展示初始化窗口
    if ini.config:
        sl = SL(ini.config[0], ini.config[1], ini.config[2])
        if not sl.restart_flag:  # 如果不重新开始
            run_flag = False
        del ini, sl
    else:
        break

