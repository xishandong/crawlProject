from drama import drama
from movie import movie
from variety import variety
import os, subprocess


def clear_screen():
    subprocess.call('cls', shell=True)


def drama_fun():
    key = input('请输入电视剧名称: ')
    d = drama(pipe)
    d.search(key)
    if d.item:
        if input('请输入1进行下载, 其他任意键回到主页面: ') == '1':
            flag = input('输入选择下载的剧集序号: ')
            ji = int(input('输入开始集数: '))
            jj = int(input('输入结束集数: '))
            clear_screen()
            d.get_m3u8_url(flag, ji, jj)
            d.download_all(ji, jj)
            clear_screen()
    else:
        clear_screen()


def movie_fun():
    key = input('请输入电影名称: ')
    m = movie(pipe)
    m.search(key)
    if m.item:
        if input('请输入1进行下载, 其他任意键回到主页面: ') == '1':
            f = input('输入选择下载的电影序号: ')
            clear_screen()
            m.get_m3u8(f)
            m.download_movie()
            clear_screen()
    else:
        clear_screen()


def variety_fun():
    key = input('请输入综艺的名称: ')
    v = variety(pipe)
    v.search(key)
    if v.item:
        flag = input('输入选择查看的综艺序号: ')
        clear_screen()
        v.print_num(flag)
        if input('请输入1进行下载, 其他任意键回到主页面: ') == '1':
            num = input('输入选择下载的期数: ')
            v.get_m3u8_urls(flag, num)
            v.download(num)
            clear_screen()
    else:
        clear_screen()


if __name__ == '__main__':
    if not os.path.exists('D:/m3u8视频'):
        os.mkdir('D:/m3u8视频')
    pipe = input('清输入选择的下载通道(0-5)\n建议通道0, 如果出现程序闪退可考虑更换通道，或者打开VPN\n')
    while True:
        choice = input('请输入想要搜索的类型(1 表示电视剧, 2 表示电影, 3 表示综艺, 其他任意键退出): ')
        clear_screen()
        if choice == '1':
            drama_fun()
        elif choice == '2':
            movie_fun()
        elif choice == '3':
            variety_fun()
        else:
            break
