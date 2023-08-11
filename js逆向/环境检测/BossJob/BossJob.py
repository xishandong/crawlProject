import time
from csv import DictWriter
from itertools import islice
from typing import Literal, Iterator, Union
from urllib.parse import urlparse, parse_qs

import execjs
import requests
from lxml import etree
from tqdm import tqdm

# ip代理信息
from boss.Proxy_info import proxies

# 类型控制
Accept = Literal['json', 'text', 'contents']
city_code_dict: dict = {'鞍山': 101070300, '阿拉善盟': 101081200, '安康': 101110700, '阿克苏地区': 101131000,
                        '阿勒泰地区': 101131500, '阿拉尔': 101131700, '阿里地区': 101140700, '安阳': 101180200,
                        '安庆': 101220600, '安顺': 101260300, '阿坝藏族羌族自治州': 101271900, '澳门': 101330100,
                        '北京': 101010100, '白城': 101060500, '白山': 101060800, '本溪': 101070500, '包头': 101080200,
                        '巴彦淖尔': 101080800, '保定': 101090200, '宝鸡': 101110900, '滨州': 101121100,
                        '巴音郭楞蒙古自治州': 101130400, '博尔塔拉蒙古自治州': 101130500, '北屯市': 101132100,
                        '白银': 101161000, '蚌埠': 101220200, '亳州': 101220900, '毕节': 101260500, '巴中': 101270900,
                        '保山': 101290300, '百色': 101301000, '北海': 101301300, '白沙黎族自治县': 101311400,
                        '保亭黎族苗族自治县': 101311800, '重庆': 101040100, '长春': 101060100, '朝阳': 101071200,
                        '赤峰': 101080500, '承德': 101090400, '沧州': 101090700, '长治': 101100500,
                        '昌吉回族自治州': 101130300, '昌都': 101140300, '常州': 101191100, '滁州': 101221000,
                        '池州': 101221500, '长沙': 101250100, '郴州': 101250500, '常德': 101250600, '成都': 101270100,
                        '潮州': 101281500, '楚雄彝族自治州': 101291700, '崇左': 101300200, '澄迈': 101311200,
                        '昌江黎族自治县': 101311500, '大庆': 101050800, '大兴安岭地区': 101051300, '大连': 101070200,
                        '丹东': 101070600, '大同': 101100200, '德州': 101120400, '东营': 101121200, '定西': 101160200,
                        '达州': 101270600, '德阳': 101271700, '东莞': 101281600, '东沙群岛': 101282200,
                        '德宏傣族景颇族自治州': 101291300, '迪庆藏族自治州': 101291500, '大理白族自治州': 101291600,
                        '儋州': 101310400, '东方': 101310900, '定安': 101311000, '鄂尔多斯': 101080600,
                        '鄂州': 101200300, '恩施土家族苗族自治州': 101201300, '抚顺': 101070400, '阜新': 101070900,
                        '阜阳': 101220800, '福州': 101230100, '抚州': 101240400, '佛山': 101280800, '防城港': 101301400,
                        '果洛藏族自治州': 101150600, '甘南藏族自治州': 101161400, '固原': 101170400, '赣州': 101240700,
                        '贵阳': 101260100, '广安': 101270800, '广元': 101271800, '甘孜藏族自治州': 101272100,
                        '广州': 101280100, '桂林': 101300500, '贵港': 101300800, '哈尔滨': 101050100, '黑河': 101050600,
                        '鹤岗': 101051100, '葫芦岛': 101071400, '呼和浩特': 101080100, '呼伦贝尔': 101080700,
                        '衡水': 101090800, '邯郸': 101091000, '汉中': 101110800, '菏泽': 101121000, '哈密': 101130900,
                        '和田地区': 101131300, '海东': 101150200, '海北藏族自治州': 101150300,
                        '黄南藏族自治州': 101150400, '海南藏族自治州': 101150500, '海西蒙古族藏族自治州': 101150800,
                        '鹤壁': 101181200, '淮安': 101190900, '黄冈': 101200500, '黄石': 101200600, '杭州': 101210100,
                        '湖州': 101210200, '合肥': 101220100, '淮南': 101220400, '淮北': 101221100, '黄山': 101221600,
                        '衡阳': 101250400, '怀化': 101251200, '惠州': 101280300, '河源': 101281200,
                        '红河哈尼族彝族自治州': 101291200, '贺州': 101300700, '河池': 101301200, '海口': 101310100,
                        '佳木斯': 101050400, '鸡西': 101051000, '吉林': 101060200, '锦州': 101070700, '晋中': 101100400,
                        '晋城': 101100600, '济南': 101120100, '济宁': 101120700, '金昌': 101160600, '酒泉': 101160800,
                        '嘉峪关': 101161200, '焦作': 101181100, '济源': 101181800, '荆州': 101200800, '荆门': 101201200,
                        '嘉兴': 101210300, '金华': 101210900, '九江': 101240200, '吉安': 101240600, '景德镇': 101240800,
                        '江门': 101281100, '揭阳': 101281900, '克拉玛依': 101130200,
                        '克孜勒苏柯尔克孜自治州': 101131100, '喀什地区': 101131200, '可克达拉市': 101132200,
                        '昆玉市': 101132300, '开封': 101180800, '昆明': 101290100, '辽源': 101060600, '辽阳': 101071000,
                        '廊坊': 101090600, '临汾': 101100700, '吕梁': 101101100, '临沂': 101120900, '聊城': 101121700,
                        '拉萨': 101140100, '林芝': 101140400, '兰州': 101160100, '陇南': 101161100,
                        '临夏回族自治州': 101161300, '洛阳': 101180900, '漯河': 101181500, '连云港': 101191000,
                        '丽水': 101210800, '六安': 101221400, '龙岩': 101230700, '娄底': 101250800, '六盘水': 101260600,
                        '泸州': 101271000, '乐山': 101271400, '凉山彝族自治州': 101272000, '临沧': 101290800,
                        '丽江': 101290900, '柳州': 101300300, '来宾': 101300400, '临高': 101311300,
                        '乐东黎族自治县': 101311600, '陵水黎族自治县': 101311700, '牡丹江': 101050300,
                        '马鞍山': 101220500, '绵阳': 101270400, '眉山': 101271500, '梅州': 101280400, '茂名': 101282000,
                        '那曲': 101140600, '南阳': 101180700, '南京': 101190100, '南通': 101190500, '宁波': 101210400,
                        '宁德': 101230300, '南平': 101230900, '南昌': 101240100, '南充': 101270500, '内江': 101271200,
                        '怒江傈僳族自治州': 101291400, '南宁': 101300100, '盘锦': 101071300, '平凉': 101160300,
                        '平顶山': 101180500, '濮阳': 101181300, '莆田': 101230400, '萍乡': 101240900,
                        '攀枝花': 101270200, '普洱': 101290500, '齐齐哈尔': 101050200, '七台河': 101050900,
                        '秦皇岛': 101091100, '青岛': 101120200, '庆阳': 101160400, '潜江': 101201500, '衢州': 101211000,
                        '泉州': 101230500, '黔东南苗族侗族自治州': 101260700, '黔南布依族苗族自治州': 101260800,
                        '黔西南布依族苗族自治州': 101260900, '清远': 101281300, '曲靖': 101290200, '钦州': 101301100,
                        '琼海': 101310600, '琼中黎族苗族自治县': 101311900, '日照': 101121500, '日喀则': 101140200,
                        '上海': 101020100, '绥化': 101050500, '双鸭山': 101051200, '四平': 101060300, '松原': 101060700,
                        '沈阳': 101070100, '石家庄': 101090100, '朔州': 101100900, '商洛': 101110600,
                        '石河子': 101131600, '双河市': 101132400, '山南': 101140500, '石嘴山': 101170200,
                        '商丘': 101181000, '三门峡': 101181700, '苏州': 101190400, '宿迁': 101191300, '十堰': 101201000,
                        '随州': 101201100, '神农架': 101201700, '绍兴': 101210500, '宿州': 101220700, '三明': 101230800,
                        '上饶': 101240300, '邵阳': 101250900, '遂宁': 101270700, '韶关': 101280200, '汕头': 101280500,
                        '深圳': 101280600, '汕尾': 101282100, '三亚': 101310200, '三沙': 101310300, '天津': 101030100,
                        '通化': 101060400, '铁岭': 101071100, '通辽': 101080400, '唐山': 101090500, '太原': 101100100,
                        '铜川': 101111000, '泰安': 101120800, '吐鲁番': 101130800, '塔城地区': 101131400,
                        '图木舒克': 101131800, '铁门关': 101132000, '天水': 101160900, '泰州': 101191200,
                        '天门': 101201600, '台州': 101210600, '铜陵': 101221200, '铜仁': 101260400, '屯昌': 101311100,
                        '台湾': 101341100, '乌海': 101080300, '乌兰察布': 101080900, '渭南': 101110500,
                        '潍坊': 101120600, '威海': 101121300, '乌鲁木齐': 101130100, '五家渠': 101131900,
                        '武威': 101160500, '吴忠': 101170300, '无锡': 101190200, '武汉': 101200100, '温州': 101210700,
                        '芜湖': 101220300, '文山壮族苗族自治州': 101291100, '梧州': 101300600, '五指山': 101310500,
                        '文昌': 101310700, '万宁': 101310800, '锡林郭勒盟': 101081000, '兴安盟': 101081100,
                        '邢台': 101090900, '忻州': 101101000, '西安': 101110100, '咸阳': 101110200, '新星市': 101132500,
                        '西宁': 101150100, '新乡': 101180300, '许昌': 101180400, '信阳': 101180600, '徐州': 101190800,
                        '襄阳': 101200200, '孝感': 101200400, '咸宁': 101200700, '仙桃': 101201400, '宣城': 101221300,
                        '厦门': 101230200, '新余': 101241000, '湘潭': 101250200, '湘西土家族苗族自治州': 101251400,
                        '西双版纳傣族自治州': 101291000, '香港': 101320300, '伊春': 101050700,
                        '延边朝鲜族自治州': 101060900, '营口': 101070800, '阳泉': 101100300, '运城': 101100800,
                        '延安': 101110300, '榆林': 101110400, '烟台': 101120500, '伊犁哈萨克自治州': 101130600,
                        '玉树藏族自治州': 101150700, '银川': 101170100, '扬州': 101190600, '盐城': 101190700,
                        '宜昌': 101200900, '宜春': 101240500, '鹰潭': 101241100, '益阳': 101250700, '岳阳': 101251000,
                        '永州': 101251300, '宜宾': 101271100, '雅安': 101271600, '云浮': 101281400, '阳江': 101281800,
                        '玉溪': 101290400, '玉林': 101300900, '张家口': 101090300, '淄博': 101120300, '枣庄': 101121400,
                        '张掖': 101160700, '中卫': 101170500, '郑州': 101180100, '周口': 101181400, '驻马店': 101181600,
                        '镇江': 101190300, '舟山': 101211100, '漳州': 101230600, '株洲': 101250300, '张家界': 101251100,
                        '遵义': 101260200, '自贡': 101270300, '资阳': 101271300, '珠海': 101280700, '肇庆': 101280900,
                        '湛江': 101281000, '中山': 101281700, '昭通': 101290700}


class BossJob:
    def __init__(self, js_name: str = '', proxy: dict = None):
        self.isFirst: bool = True  # 是否为初次访问
        self.js_name: str = js_name  # js的名称
        self.seed: str = ''  # 随机种子
        self.ts: str = ''  # 时间戳
        # api列表
        self.apiList: list[str] = [
            'https://www.zhipin.com/wapi/zpgeek/mobile/search/joblist.json',  # 职位搜索页, 需要指定params
            'https://www.zhipin.com/job_detail/',  # 不需要指定params
            f'https://www.zhipin.com/web/common/security-js/{self.js_name}.js',  # 动态加载js的链接
            'https://www.zhipin.com/wapi/zpgeek/search/joblist.json'  # web api
        ]
        # 请求头
        self.headers: dict = {
            'Accept': 'application/json, text/plain, */*',
        }
        self.cookies: dict = {}  # cookie
        self.js = execjs.compile(open('demo.js', 'r', encoding='utf-8').read())  # 调用的js
        self.stop: bool = False  # 控制手机端搜索停止
        self.checkEnd: str = ''  # 检测手机端是否爬完
        self.proxy = proxy  # 代理

    # 发送请求
    def ajax_request(self, url: str, params: dict = None, cookies=None, sleepTime: int = 5) -> requests.Response:
        for _ in range(5):
            try:
                resp = requests.get(url, params=params, headers=self.headers, cookies=cookies, timeout=10,
                                    proxies=self.proxy)
                if resp.status_code == 200:
                    return resp
                else:
                    print('HTTP Error: %s' % resp.status_code)
                    self.show_pro(sleepTime)
                    continue

            except Exception as e:
                print('出现错误: ', e)
                print('链接为: ', url)
                self.show_pro(sleepTime)
                continue
        else:
            raise Exception('超过5次也无法正常获取响应...')

    # 初始化搜索
    def first_get_seed(self, url: str, params: dict = None, isWeb: bool = False) -> Union[requests.Response, None]:
        if self.isFirst:
            resp = self.ajax_request(url=url, params=params)
            self.isFirst = False
        else:
            resp = self.ajax_request(url=url, params=params, cookies=self.cookies)
        # 未发生重定向以及是web端的情况
        if resp.url == url and not isWeb:
            print(f'=====本次没有更新cookie: {resp.url} =====')
            return resp
        elif isWeb:
            zpData = resp.json()['zpData']
            self.seed = zpData['seed']
            self.ts = zpData['ts']
            name = zpData['name']
            self.check_js(name)
            return
        # 处理重定向到检查页面的情况
        parsedUrl = urlparse(resp.url)
        generatedDict = parse_qs(parsedUrl.query)
        self.seed = generatedDict['seed'][0]
        self.ts = generatedDict['ts'][0]
        name = generatedDict['name'][0]
        self.check_js(name)

    # 手机端搜索职位
    def search_job_mobile(self, position: str, city: str, startPage: int = 1, sleepTime: int = 5) -> Iterator:
        self.headers.update({
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36',
        })
        city_code = city_code_dict.get(city)
        if city_code:
            params: dict = {
                'city': city_code,
                'query': position,
                'page': startPage
            }
            # 初始化搜索
            self.first_get_seed(self.apiList[1], params)
            self.update_cookie()
            continuations: list = [params]
            # 模拟翻页
            while continuations:
                continuation = continuations.pop()
                resp = self.ajax_request('https://www.zhipin.com/wapi/zpgeek/mobile/search/joblist.json',
                                         params=continuation, cookies=self.cookies)
                html = resp.json().get('zpData', {}).get('html')
                # 存在新的帖子
                if html and self.stop is False:
                    print(f'=====爬取{position}-{city}第{continuation["page"]}页=====')
                    continuation['page'] += 1
                    continuations.append(continuation)
                    # 提交数据
                    yield from self.parse_search_html(html)
                    # 控制爬取频率
                    self.show_pro(sleepTime)
                elif not html and self.stop is False:
                    print('=====ip被封=====')
                    continuations.append(continuation)
                    self.show_pro(sleepTime * 5)
                else:
                    print(f'=====爬取{position}-{city}停止=====')
        else:
            raise Exception(f'错误的城市名称: {city}')

    # web端搜索
    def search_job_web(self, position: str, city: str, totalPage: int = 1, sleepTime: int = 5) -> Iterator:
        self.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        })
        city_code = city_code_dict.get(city)

        if city_code:
            params = {
                'query': position,
                'city': city_code,
                'page': 1,
                'pageSize': '30',
                'scene': '1',
            }
            # 初次访问
            self.isFirst = True
            self.first_get_seed(self.apiList[3], params=params, isWeb=True)
            page = 1
            # 控制翻页
            while page <= totalPage:
                params.update({'page': page})
                self.update_cookie()
                resp = self.ajax_request(self.apiList[3], params=params, cookies=self.cookies)

                print(f'=====爬取{position}-{city}第{page}页=====')
                # 出现访问异常，重新生成cookie
                if resp.json().get('code') == 37:
                    print(f'====={resp.json().get("message")}, 正在重试 =====')
                    zpData = resp.json()['zpData']
                    self.seed = zpData['seed']
                    self.ts = zpData['ts']
                    self.show_pro(sleepTime)
                    continue
                # 出现ip被封，暂停一下
                elif resp.json().get('code') == 5002:
                    print(f'{resp.json().get("message")}')
                    self.show_pro(sleepTime * 5)
                    continue
                # 得到数据
                searchData = resp.json().get('zpData', {}).get('jobList')
                if searchData:
                    page += 1
                    # 提交管道
                    yield from self.parse_search_data(searchData)
                    # 休息一下
                    self.show_pro(sleepTime)
                # 获取下一次访问所需种子和时间戳
                self.seed = resp.cookies['__zp_sseed__']
                self.ts = resp.cookies['__zp_sts__']
        else:
            raise Exception(f'错误的城市名称: {city}')

    # 获取详情页
    def get_job_details_by_id(self, encryptJobId: str) -> str:
        self.headers.update({
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36',
        })
        url = self.apiList[1] + encryptJobId + '.html'
        return self.get_job_details_bt_url(url)

    # 获取详情页
    def get_job_details_bt_url(self, url: str, sleepTime: int = 5) -> str:
        self.headers.update({
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36',
        })
        resp = self.first_get_seed(url)
        self.update_cookie()

        if not resp:
            resp = self.ajax_request(url, cookies=self.cookies)
        tree = etree.HTML(resp.text)
        texts = tree.xpath('//div[@class="detail-content"]//text()')
        textList: list = [i.strip() for i in texts if i.strip()]

        if not textList:
            print('===== 重置cookie获取详情页 =====')
            self.isFirst = True
            self.show_pro(sleepTime)
            return self.get_job_details_bt_url(url)

        return '\n'.join(textList)

    # 保存手机端搜索结果
    def save_job_list_to_csv(self, position: str, city: str, startPage: int = 1, saveCount: int = 100):
        dataSet: Iterator = self.search_job_mobile(position, city, startPage)

        header = ['job_name', 'detail_url', 'pay', 'company_name', 'requirement']
        fp = open(f'mobile-{position}-{city}.csv', 'w', encoding='utf-8', newline='')
        writer = DictWriter(fp, header)
        writer.writeheader()

        for job in islice(dataSet, saveCount):
            job['requirement'] = ';'.join(job['requirement'])
            writer.writerow(job)

    # 保存web端搜索结果
    def save_job_list_to_csv_web(self, position: str, city: str, savePage: int = 1):
        dataSet = self.search_job_web(position, city, savePage)

        header = [
            'jobName', 'encryptJobId', 'salaryDesc', 'jobLabels', 'skills', 'jobExperience',
            'jobDegree', 'cityName', 'brandName', 'brandScaleName', 'welfareList', 'brandIndustry'
        ]
        fp = open(f'web-{position}-{city}.csv', 'w', encoding='utf-8', newline='')
        writer = DictWriter(fp, header)
        writer.writeheader()

        for job in dataSet:
            job['jobLabels'] = ';'.join(job['jobLabels'])
            job['skills'] = ';'.join(job['skills'])
            job['welfareList'] = ';'.join(job['welfareList'])
            writer.writerow(job)

    # 更新cookie
    def update_cookie(self):
        __zp = self.js.call('r', self.seed, self.ts)
        self.cookies['__zp_stoken__'] = __zp
        print(f'=====更新cookie: {self.cookies["__zp_stoken__"]}')

    # 解析手机端搜索
    def parse_search_html(self, html: str) -> Iterator:
        tree = etree.HTML(html)
        li_list = tree.xpath('//li')

        for num, li in enumerate(li_list, start=1):
            if num == 1:
                if self.checkEnd == li.xpath('./a/@href')[0]:
                    self.stop = True
                    return
                self.checkEnd = li.xpath('./a/@href')[0]

            yield {
                'job_name': li.xpath('./a/div[1]/span[1]/text()')[0],
                'detail_url': 'https://www.zhipin.com' + li.xpath('./a/@href')[0],
                'pay': li.xpath('a/div[1]/span[2]/text()')[0],
                'company_name': li.xpath('./a/div[2]/span[1]/text()')[0],
                'requirement': [r.strip() for r in li.xpath('./a/div[3]//text()') if r.strip()]
            }

    # 检查js是否为最新
    def check_js(self, name):
        if self.js_name != name:
            self.js_name = name
            print(f"=====这次的js名称 -----> {name} =====")
            resp = self.ajax_request(f'https://www.zhipin.com/web/common/security-js/{self.js_name}.js').text
            resp_ = resp.split('module,')
            resp = ''

            # 对 module 进行处理，否则容易识别为爬虫
            for i in range(len(resp_)):
                resp += resp_[i]
                if i == 0:
                    resp += 'module,'
                if i == 1:
                    resp += 'module_,'

            with open('./jssss.js', 'w', encoding='utf-8') as f:
                f.write(resp)

    @staticmethod
    # 解析web端搜索结果
    def parse_search_data(searchData: list[dict]) -> Iterator:
        for job in searchData:
            yield {
                'jobName': job['jobName'],
                'encryptJobId': job['encryptJobId'],
                'salaryDesc': job['salaryDesc'],
                'jobLabels': job['jobLabels'],
                'skills': job['skills'],
                'jobExperience': job['jobExperience'],
                'jobDegree': job['jobDegree'],
                'cityName': job['cityName'],
                'brandName': job['brandName'],
                'brandScaleName': job['brandScaleName'],
                'welfareList': job['welfareList'],
                'brandIndustry': job['brandIndustry']
            }

    @staticmethod
    # 展示休息进度条
    def show_pro(t: int, isOpen: bool = True):
        time.sleep(1)
        if isOpen:
            for _ in tqdm(
                    range(t * 10),
                    leave=False,
                    colour='blue',
                    desc='正在等待中...',
                    ascii='*-'
            ):
                time.sleep(0.1)


if __name__ == '__main__':
    boss = BossJob('a88e8dab', proxy=proxies)
    # 通过url获取详情页
    # detail = boss.get_job_details_bt_url('https://www.zhipin.com/job_detail/fc823036861698e10nF42NW0GVo~.html')
    # 通过加密id获取详情页
    # detail = boss.get_job_details_by_id('05988daddc5b6afc1n1-3du1FVZW')
    # print(detail)
    # 保存数据
    # boss.save_job_list_to_csv('python', '上海', saveCount=20)
    boss.save_job_list_to_csv_web('python', '上海', 2)
    # web搜索
    # items = boss.search_job_web('python', '上海', 5)
    # mobile搜搜
    # items = boss.search_job_mobile('python', '上海')
    # for item in items:
    #     print(item)
