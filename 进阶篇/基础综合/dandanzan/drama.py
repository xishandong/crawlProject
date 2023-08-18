import re, requests, m3u8, os, time
from concurrent.futures import ThreadPoolExecutor, wait
from urllib.parse import urljoin
from lxml import etree
import prettytable as pt
from M3U8 import M3U8


class drama:
    def __init__(self, pipe):
        # 存放m3u8链接
        self.m3u8_obj = []
        self.session = requests.Session()
        self.headers = {
            'authority': 'dandanzan.net',
            'cache-control': 'max-age=0',
            'referer': 'https://dandanzan.net',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        }
        # 定义正则表达式，匹配数字，得到已有集数
        self.r = r'\d+'
        # 存放搜索的消息
        self.item = []
        # 存放下载目录的名称
        self.dir_name = None
        # 存放下载路径
        self.pipe = int(pipe)

    def search(self, key):
        params = {
            'q': key,
        }
        response = self.session.get('https://dandanzan.net/so', params=params, headers=self.headers)
        tree = etree.HTML(response.text)
        li_list = tree.xpath('//div[@class="lists-content"]/ul/li')
        for li in li_list:
            try:
                a = li.xpath('./a/@href')[0]
                id = re.findall(self.r, a)[0]
                length = li.xpath('./a/div[1]/span/text()')[0]
                name = li.xpath('./h2/a//text()')[0]
                if length.startswith('第'):
                    s = {
                        'id': id,
                        'length': re.findall(self.r, length)[0],
                        'name': name
                    }
                    self.item.append(s)
            except:
                pass
        tb = pt.PrettyTable()
        tb.field_names = ['序号', '电视剧名称', '目前集数']
        tb.align = 'c'
        # 填充宽度
        tb.padding_width = 5
        count = 0
        for item in self.item:
            tb.add_row([count, item['name'], item['length']])
            count += 1
        print(tb)

    def get_m3u8_url(self, flag, st, et):
        id = self.item[int(flag)]['id']
        length = self.item[int(flag)]['length']
        self.dir_name = self.item[int(flag)]['name']
        if int(et) > int(length):
            raise "最大下载集数超过限制"
        for index in range(st, et + 1):
            url = f'https://dandanzan.net/fetch_plays/{id}/ep{index}'
            response = self.session.get(url)
            try:
                father_url = response.json()['video_plays'][self.pipe]['play_data']
                f_fata = m3u8.load(father_url).data
                son_url = urljoin(father_url, f_fata['playlists'][0]['uri'])
                self.m3u8_obj.append(M3U8(son_url))
                print('已获取第' + f'{index}集下载链接')
                time.sleep(0.5)
            except Exception:
                raise '出现错误，视频资源不存在'

    def create_dir(self, f):
        if not os.path.exists(f'D:/m3u8视频/{self.dir_name}'):
            os.mkdir(f'D:/m3u8视频/{self.dir_name}')
        if not os.path.exists(f'D:/m3u8视频/{self.dir_name}/第{f}集'):
            os.mkdir(f'D:/m3u8视频/{self.dir_name}/第{f}集')
        self.path = os.path.abspath(f'D:/m3u8视频/{self.dir_name}/第{f}集')

    def download_group(self, i, f):
        self.m3u8_obj[i].get_ts_url()
        total = len(self.m3u8_obj[i].ts_urls)
        self.create_dir(f)
        print(f'视频一共的分片是{total}个...')
        with ThreadPoolExecutor(max_workers=16) as executor:
            futures = []
            for j, data in enumerate(self.m3u8_obj[i].ts_urls):
                future = executor.submit(self.m3u8_obj[i].download, data, self.path, j)
                futures.append(future)
            wait(futures)
            executor.shutdown()
        self.m3u8_obj[i].merge(total, self.path)

    def download_all(self, st, et):
        flag = int(st)
        for i in range(et - st + 1):
            self.download_group(i, flag)
            flag += 1
            time.sleep(5)

