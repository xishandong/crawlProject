import time
from multiprocessing.dummy import Pool # 导入线程池模块对应的类

# # 使用单线程串行方式执行
# def get_page(str):
#     print('正在下载： ', str)
#     time.sleep(2)  # 模拟阻塞操作
#     print('下载成功： ', str)
#
#
# name_list = ['aa', 'bb', 'cc', 'dd']
# start_time = time.time()
# for i in range(len(name_list)):
#     get_page(name_list[i])
# end_time = time.time()
# print('%d second' % (end_time - start_time))


# 使用线程池的方式执行
start_time = time.time()


def get_page(str):
    print('正在下载：', str)
    time.sleep(2)  # 模拟阻塞操作
    print('下载成功：', str)


name_list = ['aa', 'bb', 'cc', 'dd']
# 实例化一个线程池对象
pool = Pool(4)
# 将列表中的每一个元素传递给get_page处理，返回值就是get_page的返回值
pool.map(get_page, name_list)
end_time = time.time()

pool.close()
pool.join()
print(end_time - start_time, 'second')
