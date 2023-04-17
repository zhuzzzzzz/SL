import numpy


def map_init(height, width, num):  # 产生一个对应地雷分布的矩阵，返回numpy的ndarray类对象
    landmine_map = numpy.hstack((numpy.ones(num, dtype=int), numpy.zeros(height * width - num, dtype=int)))
    # numpy.random.seed(0)  # 调试用代码
    numpy.random.shuffle(landmine_map)
    landmine_map = landmine_map.reshape((height, width))
    zero_ctrl_map = numpy.zeros(height * width, dtype=int)
    zero_ctrl_map = zero_ctrl_map.reshape((height, width))
    return landmine_map, zero_ctrl_map


def map_generate(init_map):  # 产生一个对应地雷分布的基于游戏规则的显示矩阵，返回numpy的ndarray类对象
    disp_map = init_map * -1
    height = init_map.shape[0]
    width = init_map.shape[1]
    for i in range(0, height):
        for j in range(0, width):
            if disp_map[i, j] == 0:
                temp = 0
                ca = _nearby_area(i, j, height, width)
                for item in ca:
                    temp = temp + init_map[item[0], item[1]]
                disp_map[i, j] = temp
    return disp_map


def _nearby_area(r, c, height, width):
    # 返回可计算的方块坐标，若是边缘方块，则返回可计算部分的方块坐标，height,width>=3
    # 输出数据格式：{(7, 0), (7, 1), (8, 0), (8, 1)}
    around_set = []
    if r == 0:
        around_set.append({(r, c - 1), (r, c), (r, c + 1), (r + 1, c - 1), (r + 1, c), (r + 1, c + 1)})  # 当前行和下一行
    if r == height - 1:
        around_set.append({(r - 1, c - 1), (r - 1, c), (r - 1, c + 1), (r, c - 1), (r, c), (r, c + 1)})  # 上一行和当前行
    if c == 0:
        around_set.append({(r - 1, c), (r, c), (r + 1, c), (r - 1, c + 1), (r, c + 1), (r + 1, c + 1)})  # 当前列和右侧列
    if c == width - 1:
        around_set.append({(r - 1, c - 1), (r, c - 1), (r + 1, c - 1), (r - 1, c), (r, c), (r + 1, c)})  # 左侧列和当前列
    if len(around_set) < 1:
        return {(r - 1, c - 1), (r - 1, c), (r - 1, c + 1), (r, c - 1), (r, c), (r, c + 1), (r + 1, c - 1), (r + 1, c),
                (r + 1, c + 1)}
    elif len(around_set) == 1:
        return around_set[0]
    else:
        res = {(r - 1, c - 1), (r - 1, c), (r - 1, c + 1), (r, c - 1), (r, c), (r, c + 1), (r + 1, c - 1), (r + 1, c),
               (r + 1, c + 1)}
        for i in around_set:
            res = res & i  # 求交集s
        return res


def _check_value(obj, r, c):
    return obj[r, c]


def _set_value(obj, r, c, value):
    obj[r, c] = value


def _get_coordinate(obj, r, c, value):
    na = _nearby_area(r, c, obj.shape[0], obj.shape[1])
    res = set()
    len(res)
    for item in na:
        if obj[item[0], item[1]] == value:
            res.add(item)
    return res

# print(map_generate(map_init(9, 9, 10)[0]))
# print(m0)
# _set_value(m0, 0, 0, 10)
# print(m0)
# print(_check_value(m0, 0, 0))
