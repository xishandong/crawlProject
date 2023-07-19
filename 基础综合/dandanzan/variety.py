import m3u8, re
from movie import movie
from lxml import etree
import prettytable as pt
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, wait
from M3U8 import M3U8


class variety(movie):
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
                length = li.xpath('./a/div[1]/span/text()')[0].strip()
                name = li.xpath('./h2/a//text()')[0].strip()
                s = {
                    'url': 'https://dandanzan.net' + a,
                    'id': id,
                    'length': length,
                    'name': name
                }
                self.item.append(s)
            except:
                pass
        tb = pt.PrettyTable()
        tb.field_names = ['序号', '综艺名称', '最新一期']
        tb.align = 'c'
        # 填充宽度
        tb.padding_width = 5
        count = 0
        for item in self.item:
            tb.add_row([count, item['name'], item['length']])
            count += 1
        print(tb)

    def get_m3u8_urls(self, flag, num):
        id = self.item[int(flag)]['id']
        length = num
        self.dir_name = self.item[int(flag)]['name']
        url = f'https://dandanzan.net/fetch_plays/{id}/{length}'
        response = self.session.get(url)
        try:
            father_url = response.json()['video_plays'][self.pipe]['play_data']
            f_fata = m3u8.load(father_url).data
            son_url = urljoin(father_url, f_fata['playlists'][0]['uri'])
            self.m3u8_obj.append(M3U8(son_url))
            print('下载链接已获取')
        except Exception:
            raise '出现错误，电影资源不存在'

    def print_num(self, flag):
        url = self.item[int(flag)]['url']
        resp = self.session.get(url, headers=self.headers)
        tree = etree.HTML(resp.text)
        li_list = tree.xpath('//ul[@id="eps-ul"]/li')
        num = []
        for li in li_list:
            number = li.xpath('./@ep_slug')[0]
            num.append(number)
        table = pt.PrettyTable()
        table.field_names = ['期数1', '期数2', '期数3', '期数4', '期数5']
        # 计算需要填充的空值数量
        num_padding = 5 - len(num) % 5
        # 填充空值
        num += [None] * num_padding
        for i in range(0, len(num), 5):
            table.add_row([*num[i:i + 5]])
        print(table)

    def download(self, num):
        self.m3u8_obj[0].get_ts_url()
        total = len(self.m3u8_obj[0].ts_urls)
        self.create_dir(num)
        print(f'视频一共的分片是{total}个...')
        with ThreadPoolExecutor(max_workers=16) as executor:
            futures = []
            for j, data in enumerate(self.m3u8_obj[0].ts_urls):
                future = executor.submit(self.m3u8_obj[0].download, data, self.path, j)
                futures.append(future)
            wait(futures)
            executor.shutdown()
        self.m3u8_obj[0].merge(total, self.path)
