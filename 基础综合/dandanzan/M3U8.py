import time
import m3u8, requests, os
from urllib.parse import urljoin
from Crypto.Cipher import AES
from requests.exceptions import RequestException


class M3U8:
    def __init__(self, url):
        self.decryptor = None
        self.url = url
        self.count = 0
        self.ts_urls = []

    def get_ts_url(self):
        son_url = self.url
        key_url = None
        r = m3u8.load(son_url).data
        self.ts_urls = [urljoin(son_url, ts['uri']) for ts in r['segments']]
        try:
            if r['segments'][0]['key']['uri'].startswith('h' or 'H'):
                key_url = r['segments'][0]['key']['uri']
            else:
                key_url = urljoin(son_url, r['segments'][0]['key']['uri'])
        except:
            pass
        if key_url:
            key = requests.get(key_url).content
            self.decryptor = AES.new(key, AES.MODE_CBC, b'\x00' * 16)
        else:
            self.decryptor = None

    def download(self, url, path, index, retry_times=5):
        for i in range(retry_times):
            try:
                resp = requests.get(url, timeout=60)
                if resp.status_code == 200:
                    with open(path + f'\\{index}.ts', 'wb') as f:
                        if self.decryptor:
                            f.write(self.decryptor.decrypt(resp.content))
                        else:
                            f.write(resp.content)
                    self.count += 1
                    if self.count % 100 == 0:
                        print(f'已经下载{self.count}个分片了!')
                    return True
            except RequestException as e:
                print(f"Download failed: {url}\n{e}\nretrying ({i + 1}/{retry_times})...")
                time.sleep(5)
        raise RequestException(f"Failed to download {url} after {retry_times} retries.")

    @staticmethod
    def merge(total, path):
        with open(path + '\\video.mp4', 'ab') as fp:
            for index in range(total):
                try:
                    f = path + f'\\{index}.ts'
                    content = open(f, 'rb').read()
                    fp.write(content)
                    os.remove(path + f'\\{index}.ts')
                except Exception as e:
                    print(e)
