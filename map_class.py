import copy
from map_func import *
from map_func import _set_value, _check_value, _nearby_area, _get_coordinate


class Map:  # 游戏地图底层逻辑类
    def __init__(self, height, width, num):
        # 游戏过程中静态变量
        self.height = height
        self.width = width
        self.num = num
        self.landmine_map = map_init(self.height, self.width, self.num)[0]  # 地雷地图，只读
        self.disp_map = map_generate(self.landmine_map)  # 基于游戏规则的地雷显示地图，只读

        # 游戏过程中动态变量
        self.disp_ctrl_map = map_init(self.height, self.width, self.num)[1]  # 全0显示控制地图，可读写
        self.mark_ctrl_map = copy.deepcopy(self.disp_ctrl_map)  # 全0标记控制地图，可读写，要用到拷贝，不然值会一起变化！
        self.bomb_left = self.num  # 当前剩余地雷数

    # def explore_map(self, r, c):  # 探索未知方块
    #     _set_value(self.disp_ctrl_map, r, c, 1)
    #     _set_value(self.mark_ctrl_map, r, c, 0)  # 当方块处于显示状态时，必须消除标记！
    #     ans = _check_value(self.disp_map, r, c)
    #     if ans == -1:  # 若踩雷则返回False,r,c,-1
    #         return {(False, r, c, -1)}
    #     elif ans == 0:  # 当值为0时打开周围方块，返回被True及打开的方块坐标及对应的值
    #         res = set()
    #         for item in _nearby_area(r, c, self.height, self.width):
    #             _set_value(self.disp_ctrl_map, item[0], item[1], 1)
    #             _set_value(self.mark_ctrl_map, item[0], item[1], 0)
    #             res.add((True, item[0], item[1], _check_value(self.disp_map, item[0], item[1])))
    #         return res
    #     else:  # 获取当前方块值
    #         return {(True, r, c, ans)}

    def explore_map(self, r, c):  # 探索未知方块
        _set_value(self.disp_ctrl_map, r, c, 1)
        _set_value(self.mark_ctrl_map, r, c, 0)  # 当方块处于显示状态时，消除标记！
        ans = _check_value(self.disp_map, r, c)
        if ans == -1:  # 若踩雷则返回False,r,c,-1
            return {(False, r, c, -1)}
        elif ans == 0:  # 当值为0时打开周围方块，返回被True及打开的方块坐标及对应的值
            res = set()
            for item in _nearby_area(r, c, self.height, self.width):
                # 若打开方块为0，则需要进一步处理周边方块，且当前方块已设置显示位并消除了标记位
                # 如果周边的方块里有0值，并且处于未显示状态，则递归地调用本函数打开所有的可显示方块
                # （每一次调用当前方块都设置了显示位，在下面增加相关的判断条件，可以防止程序无限递归调用！）
                if _check_value(self.disp_map, item[0], item[1]) == 0 and _check_value(self.disp_ctrl_map, item[0],
                                                                                       item[1]) == 0:
                    for i in self.explore_map(item[0], item[1]):
                        res.add(i)  # 此时打开的都是0值方块，结果直接添加进集合就行了
                # 递归部分结束
                res.add((True, item[0], item[1], _check_value(self.disp_map, item[0], item[1])))
                _set_value(self.disp_ctrl_map, item[0], item[1], 1)  # 在操作完成后要把这个方块的状态置为可见，否则会陷入无限递归调用！
                _set_value(self.mark_ctrl_map, item[0], item[1], 0)
            return res
        else:  # 获取当前方块值
            return {(True, r, c, ans)}


    def mark_map(self, r, c):  # 标记地图
        # 标记1次为插旗，标记2次为问号，标记3次重置
        if _check_value(self.disp_ctrl_map, r, c) == 0:  # 当且仅当方块处于未显示状态时才能标记！
            res = _check_value(self.mark_ctrl_map, r, c)
            if res == 0:
                _set_value(self.mark_ctrl_map, r, c, 1)
            elif res == 1:
                _set_value(self.mark_ctrl_map, r, c, 2)
            else:
                _set_value(self.mark_ctrl_map, r, c, 0)
            pass
            return r, c, _check_value(self.mark_ctrl_map, r, c)
        else:
            return None

    def clear_mine(self, r, c):  # 标记地雷后排雷
        # 点击已显示的有数字地图才有效，否则返回None
        if _check_value(self.disp_ctrl_map, r, c) == 1 and _check_value(self.disp_map, r, c) >= 1:
            undisplayed = _get_coordinate(self.disp_ctrl_map, r, c, 0)  # 未显示的方块坐标
            unfinded = undisplayed & _get_coordinate(self.disp_map, r, c, -1)  # 未显示的与地雷的交集：未发现的地雷坐标
            marked = _get_coordinate(self.mark_ctrl_map, r, c, 1)  # 已标记的
            if len(marked) == len(unfinded):  # 当点击位置周围应有的 -隐藏地雷数- 等于 -已标记地雷数-，可以开始排雷；否则返回None
                # 开始排雷
                for item in _nearby_area(r, c, self.height, self.width):  # 首先将附近全部区域设为可见
                    _set_value(self.disp_ctrl_map, item[0], item[1], 1)
                    _set_value(self.mark_ctrl_map, item[0], item[1], 0)
                res = set()
                flag = True
                for item in undisplayed:  # 输出每个位置的排雷情况
                    if (item in marked) and (item not in unfinded):  # 如果未显示的方块是被标记的，但不是未发现的地雷，赋错值
                        flag = False
                        res.add((False, item[0], item[1], _check_value(self.disp_map, item[0], item[1])))
                    else:
                        res.add((True, item[0], item[1], _check_value(self.disp_map, item[0], item[1])))
                if flag:  # 如果排雷未出错
                    self.bomb_left = self.bomb_left - len(marked)  # 全部标记正确，更新当前剩余地雷数
                    # 调用self.explore_map递归打开所有值为0的方块
                    temp = copy.deepcopy(res)  # 为防止出现异常使用深拷贝
                    for item in temp:
                        if item[3] == 0:  # 如果该打开的方块值为0
                            for i in self.explore_map(item[1], item[2]):
                                res.add((True, i[1], i[2], _check_value(self.disp_map, i[1], i[2])))
                pass
                return res
            else:
                return None
        else:
            return None

    def is_clear(self):  # 若剩余未显示的方块数等于剩余地雷数，游戏胜利
        if self.height * self.width - self.disp_ctrl_map.sum() == self.bomb_left:
            return True
        else:
            return False
