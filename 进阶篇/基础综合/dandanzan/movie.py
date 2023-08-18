import m3u8, re
from lxml import etree
from M3U8 import M3U8
from drama import drama
import prettytable as pt
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, wait


class movie(drama):
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
                if not length.startswith('第'):
                    s = {
                        'id': id,
                        'length': length,
                        'name': name
                    }
                    self.item.append(s)
            except:
                pass
        tb = pt.PrettyTable()
        tb.field_names = ['序号', '电影名称', '清晰度']
        tb.align = 'c'
        # 填充宽度
        tb.padding_width = 5
        count = 0
        for item in self.item:
            tb.add_row([count, item['name'], item['length']])
            count += 1
        print(tb)

    def get_m3u8(self, flag):
        id = self.item[int(flag)]['id']
        length = 'hd'
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

    def download_movie(self):
        self.m3u8_obj[0].get_ts_url()
        total = len(self.m3u8_obj[0].ts_urls)
        self.create_dir(1)
        print(f'视频一共的分片是{total}个...')
        with ThreadPoolExecutor(max_workers=16) as executor:
            futures = []
            for j, data in enumerate(self.m3u8_obj[0].ts_urls):
                future = executor.submit(self.m3u8_obj[0].download, data, self.path, j)
                futures.append(future)
            wait(futures)
            executor.shutdown()
        self.m3u8_obj[0].merge(total, self.path)
