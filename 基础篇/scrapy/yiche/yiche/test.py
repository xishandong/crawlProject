import json


def detail(fp):
    res = json.loads(fp)
    k = 0
    car = []  # 存储所有车辆的所有信息
    name_list = []  # 存储参数的名称

    while k < len(res['data']):
        if k >= 3:  # 控制获取信息到目录的第几级
            break
        else:
            item_list = res["data"][k]["items"]

        value_list = []
        car_list = []

        for item in item_list:
            # 车辆颜色需要专门写
            if item['id'] == -30 or item['id'] == -31:
                break
            else:
                name_list.append(item['name'])
                value_list.append(item['paramValues'])

        for value in value_list:
            i = 0
            while i < len(value):
                va = value[i]['value']
                if va == '-':
                    va = value[i]['subList'][0]['value']
                car_list.append(va)
                i += 1
            car.append(car_list)
            car_list = []
        k += 1

    # 规范汽车参数格式
    forN = len(car)  # 参数的个数
    carN = len(car[1])  # 车辆的个数
    car = sum(car, [])  # 整合汽车信息
    time = 0  # 循环次数
    a = []
    b = []
    name0 = []

    while time < carN:
        x = time
        k = 0
        for i in range(forN):
            if k == 0:
                name0.append(car[x])
            else:
                c = name_list[k] + ':' + car[x]
                a.append(c)
            x += carN
            k += 1
        time += 1
        b.append(a)
        a = []

    s = []

    for k in b:
        k = ' '.join(k)
        s.append(k)
    sk = {
        'detail': s,
        'name': name0
    }
    return sk

