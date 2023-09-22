import execjs
import requests
from tqdm import tqdm
import csv
import os

xx = '010001'
yy = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
zz = '0CoJUm6Qyw8W8jud'
cookies = {
    'MUSIC_U': '',
}
headers = {
    'authority': 'music.163.com',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
    # 'cookie': 'P_INFO=18608219667|1659842485|1|study|00&99|null&null&null#sic&510500#10#0|&0||18608219667; __bid_n=184855102dc3deb72f4207; FPTOKEN=72X4JbpCu5OusTIYuHrCSGgjkuVlm7w0d2wuZhf+LU7tCP8d2MdyrBKXbvhWmMBQ4PKKvkagbJ51CrfoDP1FK92ujmpUvUgInBgFojtQGyau97Tpz4WSuTnUiS6fizwTsHkskf4I2RdqrQCBQFHtYEtOnpD8RQadQBQbKXjwRw/nR1DO+23Y6vcDZbzGXAtLl6Xm4RhhE95S1srhGEVyjbIKGwnyHfiAJRmy6s7aRwJy06lrHyqXmRGsl75msfYuOSPVdoqKR50yZOaIXkE9+reLCp71sfWzH6IyIuEd0tOfp2DIGQOXRwPNsfJIVhnzOmQETOjXTciGSjjqjpcB1HvV6MJEPoJTz9jtA9xEAbpdqzfdbXWd1t66tiWvMdSwOdRJufrVWLb5Kp45jXCEMg==|4i8C4fx+LJpM3RJOqHD5D/gktdXKtOZsPzv+3ONA2vU=|10|4784ce007f1eaa4073c5660cfcf93bfa; vinfo_n_f_l_n3=0f5eba99d02a8a90.1.12.1673163354239.1673496764827.1673499976392; _iuqxldmzr_=32; _ntes_nnid=f37f7a44b589883a8947dd6fca21229a,1674451825593; _ntes_nuid=f37f7a44b589883a8947dd6fca21229a; NMTID=00OpWJ6K25R-OBw305HoKc7iw1Bum4AAAGF3Rs0ZA; WEVNSM=1.0.0; WNMCID=pozalx.1674451825917.01.0; WM_TID=%2BrY9QzhJ44xAQUUBAFKBIufmFp9POPoJ; WM_NI=FZifNkYxQ5%2BsOc7UcO0iL2%2BysJb4NBTGZYVM84rxk4hET0mDURlUNWjbwIRjhuX5QLHgQRO1zicH%2BhhGxyGw5XoZKrhco9d3otC6cYq4jWsQGVO9ozzTlzitaHjcs4mocU0%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeb0cf6f898e0096fc4eada88fb2d54f838a9fadc147edb99d98bc46bab7a9abe52af0fea7c3b92a8686a787cd619ba89fd6aa798dbdf9b6e245f4b784d3aa73b196aed5cd4a989996bad547fcecbe99ea40ac9b9cd1f050978ea4b6cd5daabeb9aad162acab98d6d4488cb99fb3ce3bbab7ada9aa64ac99b89ac67df788a1bbca7aacbda1dae739adac8dd7e253b3eca6b8f25b858a81daee72ba8ca49bec80a398a684f240afb1adb6b337e2a3; playerid=49334466; JSESSIONID-WYYY=o%5CyijWemMcjioZJ1fsF%5C9sl57SgrkFa6o9yMUd4dnNshvo11uAMNJOV%5CbIJYe0VSo2xpDI0mc%2FUvQX2xQpe1U2JCJDfEwIvO%2FhMo%5CGHCcfZI3r%2BzseRcOnnrt8NsZwR53VNvUYHNp6sYzWTZEiYbYJ9D4%2Fv%2BIUCnGPv3mypr1JBIDaev%3A1674532481499',
    'origin': 'https://music.163.com',
    'referer': 'https://music.163.com/',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}
params = {
    'csrf_token': ''
}


def replace_lastChar(former_str, replacechar):
    return former_str[:-1] + replacechar


def returnError(response):
    if response.json()['result'] == {}:
        print('搜索的内容无法查找到!')
        return 0


def downloader(url, i3x, id):
    param = execjs.compile(open('demo.js', 'r', encoding='utf-8').read()).call('d', i3x, xx, yy, zz)
    data = {
        'params': param['encText'],
        'encSecKey': param['encSecKey']
    }
    response = requests.post(
        url,
        params=params,
        cookies=cookies,
        headers=headers,
        data=data,
    )
    try:
        url = response.json()['data']['url']
    except:
        url = response.json()['urls'][0]['url']
    res = requests.get(url, stream=True)
    content_size = int(res.headers['Content-Length']) / 1024
    print('正在下载MV。。。')
    with open(f'./MV/{id}.mp4', 'wb') as fp:
        for data in tqdm(iterable=res.iter_content(1024),
                         total=content_size,
                         unit='k'):
            fp.write(data)
    print('下载完成！')


def searchLoader(i3x, name, offset):
    i3x = format(i3x % (name, offset))
    param = execjs.compile(open('demo.js', 'r', encoding='utf-8').read()).call('d', i3x, xx, yy, zz)
    data = {
        'params': param['encText'],
        'encSecKey': param['encSecKey']
    }
    response = requests.post(
        'https://music.163.com/weapi/cloudsearch/get/web',
        params=params,
        cookies=cookies,
        headers=headers,
        data=data,
    )
    return response


def Post(time, id, i, key):
    if key == 1:
        i3x = {
            'csrf_token': "d5e1f281f7b6f7ff2caf0af810f347d7",
            'cursor': str(time),
            'offset': "0",
            'orderType': "2",
            'pageNo': f"{i}",
            'pageSize': "20",
            'rid': f"R_SO_4_{id}",
            'threadId': f"R_SO_4_{id}",
        }
    elif key == 2:
        if len(id) == 32:
            i3x = {
                'csrf_token': "d5e1f281f7b6f7ff2caf0af810f347d7",
                'cursor': str(time),
                'offset': "0",
                'orderType': "1",
                'pageNo': f"{i}",
                'pageSize': "20",
                'rid': f"R_VI_62_{id}",
                'threadId': f"R_VI_62_{id}",
            }
        else:
            i3x = {
                'csrf_token': "d5e1f281f7b6f7ff2caf0af810f347d7",
                'cursor': str(time),
                'offset': "0",
                'orderType': "1",
                'pageNo': f"{i}",
                'pageSize': "20",
                'rid': f"R_MV_5_{id}",
                'threadId': f"R_MV_5_{id}",
            }
    param = execjs.compile(open('demo.js', 'r', encoding='utf-8').read()).call('md', i3x, xx, yy, zz)
    data = {
        'params': param['encText'],
        'encSecKey': param['encSecKey']
    }
    response = requests.post('https://music.163.com/weapi/comment/resource/comments/get', params=params,
                             headers=headers, data=data, cookies=cookies)
    return response.json()


def getCursor(datas):
    userInfos = datas["data"]["comments"]
    if len(userInfos) < 20:
        return 'end'
    userInfo = userInfos[19]['time']
    return userInfo


def comment(datas):
    userInfos = datas["data"]["comments"]
    infos = []
    userInfo = {}
    for info in userInfos:
        info1 = info["user"]
        if info1["vipRights"] is not None:
            userInfo = {
                '评论人的ID': info1['userId'],
                '评论人网名': info1['nickname'],
                '评论人VIP等级': info1["vipRights"]['redVipLevel'],
                '评论人头像网址': info1['avatarUrl'],
                '评论编号': info['commentId'],
                '评论时间': info['timeStr'],
                '点赞量': info['likedCount'],
                '评论内容': info['content'],
                'ip地址': info["ipLocation"]['location']
            }
        else:
            userInfo['评论人VIP等级'] = 0
        infos.append(userInfo)
    return infos


def get_comment(endNum, id, key):
    header = ['评论人的ID', '评论人网名', '评论人VIP等级', '评论人头像网址', '评论编号', '评论时间', '点赞量',
              '评论内容', 'ip地址']
    fp = open(f'./comment/comment_of_{id}.csv', 'w', encoding='utf-8', newline='')
    writer = csv.DictWriter(fp, header)
    writer.writeheader()
    id = str(id)
    i = 1
    data = Post(-1, id, i, key)
    while True:
        time = getCursor(data)
        info = comment(data)
        writer.writerows(info)
        print('正在下载第', i, '页的评论')
        if time == 'end' or i == endNum:
            break
        i += 1
        data = Post(time, id, i, key)
    fp.close()


def get_lyric(id):
    i3x = '{"id":"%d","lv":-1,"tv":-1,"csrf_token":"d5e1f281f7b6f7ff2caf0af810f347d7"}'
    i3x = format(i3x % id)
    param = execjs.compile(open('demo.js', 'r', encoding='utf-8').read()).call('d', i3x, xx, yy, zz)
    data = {
        'params': param['encText'],
        'encSecKey': param['encSecKey']
    }
    response = requests.post('https://music.163.com/weapi/song/lyric', params=params, cookies=cookies, headers=headers,
                             data=data)
    res = response.json()["lrc"]['lyric']
    try:
        resp = response.json()["tlyric"]['lyric']
    except:
        resp = ''
    with open(f'./lyric/lyric_of_{id}.txt', 'w', encoding='utf-8') as fp:
        fp.write(res)
        if resp != '':
            fp.write('译文如下所示\n')
            fp.write(resp)


def get_musicUrl(mid):
    i3x = '{"ids":"[%d]","level":"lossless","encodeType":"aac","csrf_token":"d5e1f281f7b6f7ff2caf0af810f347d7"}'
    i3x = format(i3x % mid)
    param = execjs.compile(open('demo.js', 'r', encoding='utf-8').read()).call('d', i3x, xx, yy, zz)
    data = {
        'params': param['encText'],
        'encSecKey': param['encSecKey']
    }
    response = requests.post(
        'https://music.163.com/weapi/song/enhance/player/url/v1',
        params=params,
        cookies=cookies,
        headers=headers,
        data=data,
    )
    Url = response.json()["data"][0]['url']
    if Url is None:
        return 'error'
    return Url


def GetMusic(url, mid):
    if url != 'error':
        response = requests.get(
            url=url,
            headers=headers,
            stream=True
        )
        if str(response) == '<Response [403]>':
            new_url = replace_lastChar(url, 'r')
            response = requests.get(
                url=new_url,
                headers=headers,
                stream=True
            )
        content_size = int(response.headers['Content-Length']) / 1024
        print('正在下载歌曲。。。')
        with open(f'./music/{mid}.mp3', 'wb') as fp:
            for data in tqdm(iterable=response.iter_content(1024),
                             total=content_size,
                             unit='k'):
                fp.write(data)
        print('下载完成！')
    else:
        print('歌曲暂无音源或需要购买专辑才能下载')


def searchSong(name, offset):
    i3x = '{"hlpretag":"<span class=\\"s-fc7\\">","hlposttag":"</span>","id":"160947","s":"%s","type":"1","offset":"%d","total":"true","limit":"30","csrf_token":"ee74402ef50d2a957bccb7b540f4bc27"}'
    response = searchLoader(i3x, name, offset)
    if returnError(response) == 0:
        return 0
    total = response.json()["result"]['songCount']
    songs = response.json()['result']['songs']
    print('搜索到的结果有', total, '条')
    for song in songs:
        songInfo = {
            '歌曲id': song['id'],
            '歌曲名称': song['name'],
            '歌手姓名': song['ar'][0]['name'],
            '专辑名称': song['al']['name'],
            'mvid': song['mv']
        }
        print(songInfo)
    return total


def searchFunction(flag):
    name = input('请输入想要搜索的内容:\n')
    offset = 0
    while True:
        if flag == '1':
            total = searchSong(name, offset)
        elif flag == '2':
            total = searchMV(name, offset)
        else:
            print('错误的输入，请按提示进行输入')
            break
        offset += 30
        if offset > total:
            print('已超出上线，退出搜索功能\n')
            break
        keys = input(f'是否继续搜索，输入任意字符继续搜索{name}下一页的内容，退出请输入0\n')
        if keys == '0':
            break


def downloadFunction(flag):
    if flag == '3':
        id = input('请输入想要下载的歌曲id\n')
        id = int(id)
        while True:
            keys = input('请输入想要进行的操作: 1.下载歌曲 2.下载歌词 3.下载评论 0.退出\n')
            if keys == '1':
                print('重复下载将会覆盖之前下载的文件')
                url = get_musicUrl(id)
                GetMusic(url, id)
            elif keys == '2':
                print('重复下载将会覆盖之前下载的文件')
                get_lyric(id)
            elif keys == '3':
                print('重复下载将会覆盖之前下载的文件')
                num = input('请输入下载评论的页数\n')
                get_comment(int(num), id, 1)
            elif keys == '0':
                break
            else:
                print('错误输入，请重新输入')
                continue
    elif flag == '4':
        id = input('请输入想要下载的MV的id:\n')
        while True:
            keys = input('请输入想要进行的操作: 1.下载MV 2.下载评论 0.退出\n')
            if keys == '1':
                print('重复下载将会覆盖之前下载的文件')
                downloadMV(id)
            elif keys == '2':
                print('重复下载将会覆盖之前下载的文件')
                num = input('请输入下载评论的页数\n')
                get_comment(int(num), id, 2)
            elif keys == '0':
                break
            else:
                print('错误输入，请重新输入')
                continue


def searchMV(name, offset):
    i3x = '{"hlpretag":"<span class=\\"s-fc7\\">","hlposttag":"</span>","id":"160947","s":"%s","type":"1014","offset":"%d","total":"true","limit":"20","csrf_token":"ee74402ef50d2a957bccb7b540f4bc27"}'
    response = searchLoader(i3x, name, offset)
    if returnError(response) == 0:
        return 0
    total = response.json()["result"]['videoCount']
    videos = response.json()['result']['videos']
    print('搜索到的结果有', total, '条')
    for video in videos:
        MVInfo = {
            'MV的id': video['vid'],
            'MV名称': video['title'],
        }
        print(MVInfo)
    return total


def downloadMV(id):
    if len(id) == 32:
        i3x = '{"ids":"[\\"%s\\"]","resolution":"1080","csrf_token":"ee74402ef50d2a957bccb7b540f4bc27"}'
        i3x = format(i3x % id)
        url = 'https://music.163.com/weapi/cloudvideo/playurl'
        downloader(url, i3x, id)
    else:
        id = int(id)
        i3x = '{"id":"%d","r":"1080","csrf_token":"ee74402ef50d2a957bccb7b540f4bc27"}'
        i3x = format(i3x % id)
        url = 'https://music.163.com/weapi/song/enhance/play/mv/url'
        downloader(url, i3x, id)


def checkDir():
    if not os.path.exists('music'):
        os.mkdir('music')
    if not os.path.exists('MV'):
        os.mkdir('MV')
    if not os.path.exists('lyric'):
        os.mkdir('lyric')
    if not os.path.exists('comment'):
        os.mkdir('comment')


if __name__ == '__main__':
    checkDir()
    while True:
        print('欢迎使用音乐下载器')
        key = input('请输入想要选择的功能: 1.搜索歌曲 2.搜索MV 3.下载歌曲 4.下载MV 0.退出程序\n')
        if key == '1':
            searchFunction(key)
        elif key == '2':
            searchFunction(key)
        elif key == '3':
            downloadFunction(key)
        elif key == '4':
            downloadFunction(key)
        elif key == '0':
            break
        else:
            print('错误输入，请重新输入')
            continue
