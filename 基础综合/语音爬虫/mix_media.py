import os
import re


def get(dir_path):
    file_list = os.listdir(dir_path)
    # file_list.sort(key=lambda i: int(re.match(r'(\d+)', i).group()))
    contents = []
    for cur_file in file_list:
        path = os.path.join(os.path.abspath(dir_path), cur_file)
        with open(path, 'rb') as fp:
            content = fp.read()
            contents.append(content)
        # os.remove(path)
        print(path)
    with open(f'{dir_path}/all.mp4', 'wb') as f:
        for c in contents:
            f.write(c)


if __name__ == '__main__':
    path = input('请输入目录:\n')
    get(path)
