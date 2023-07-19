from baidu import baidu
from youdao import youdao


if __name__ == '__main__':
    while True:
        flag = input('请选择来源:(1.百度 2.有道 3.退出)\n')
        if flag == '3':
            break
        path = input('请输入文件路径:\n')
        lan = input('请输入文件语言:(zh, en, kr/kor[有道, 百度])\n')
        if flag == '1':
            baidu(path, lan)
        elif flag == '2':
            youdao(path, lan)
