import json
import re
import time
from urllib.parse import quote

import execjs
import prettytable as pt
import requests

from acw_tc_3 import get_226, replace_info


class CEAir:
    def __init__(self):
        self.headers = {
            'Origin': 'https://m.ceair.com',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        }
        self.cookies = {}

        self.session = requests.Session()
        self.flag = 1
        self.get_acw_tc()

    def get_acw_tc(self):
        resp = self.session.get('https://m.ceair.com/mapp/Home', headers=self.headers)
        acw_tc = resp.cookies.get('acw_tc')
        if acw_tc:
            self.cookies['acw_tc'] = acw_tc

    def ajax_request(self, *, url, json_data, params: dict) -> json:
        """
        # 发送请求
        :param params:params参数
        :param url: api接口
        :param json_data: 表单信息
        :return: json数据
        """
        refer = execjs.compile(open('refer_1306.js', 'r', encoding='utf-8').read()).call('getRefer', json_data)
        if not params:
            par = {
                'refer__1036': refer
            }
        else:
            params['refer__1036'] = refer
            par = params
        resp = self.session.post(url=url, params=par, json=json_data, headers=self.headers, cookies=self.cookies)
        acw_sc_v3 = resp.cookies.get('acw_sc__v3')
        acw_tc = resp.cookies.get('acw_tc')
        if acw_tc:
            self.cookies['acw_tc'] = acw_tc
        if acw_sc_v3:
            self.cookies['acw_sc__v3'] = acw_sc_v3
        try:
            data = resp.json()['res']
            ctx = execjs.compile(open('./demo.js', 'r', encoding='utf-8').read()).call('decrypto', data)
            return json.loads(ctx)
        except requests.exceptions.JSONDecodeError:
            # 处理acw_sc
            par = self.cookie_update(resp.text, par)
            return self.ajax_request(url=url, json_data=json_data, params=par)

    def get_flight(self, arr, dep, date):
        """
        :param arr: 到达城市
        :param dep: 出发城市
        :param date: 出发时间
        :return: 返回航班信息
        """
        data = {
            "tripType": 0, "depCode": self.get_city_code(dep), "arrCode": self.get_city_code(arr), "dt": "1", "at": "1",
            "depN": dep, "arrN": arr,
            "flightDate": date, "carryChd": False, "carryInf": False, "productType": "CASH", "curIndex": 0
        }
        url = quote(json.dumps(data, separators=(',', ':')))
        url = 'https://m.ceair.com/mapp/reserve/flightList?newParam=' + url
        self.headers.update({
            'Content-Type': 'application/json',
            'M-CEAIR-ENCRYPTED': 'true',
            'Origin': 'https://m.ceair.com',
            'Referer': url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'X-CEAIR-OS': 'M',
            'transactionId': '05202304231034048094',
        })
        json_data = {
            "currentQueryType": "FLIGHT_LIST", "currentSegIndex": 0, "carryChd": False, "carryInf": False,
            "productCodes": [],
            "selectedRoutes": [], "productType": "CASH",
            "routes": [{"arrCode": data['arrCode'], "depCode": data['depCode'], "flightDate": data['flightDate'],
                        "arrCodeType": data['at'], "depCodeType": data['dt'], "depCityName": data['depN'],
                        "arrCityName": data['arrN'], "segIndex": 0}],
            "tripType": "OW", "cabinGrade": "", "memberLabel": "", "salesChannel": "7701", "moduleX": "mShopping",
            "os": "M",
            "appVersion": "99.0.0", "transactionId": "05202304231034048094"
        }
        a = json.dumps(json_data, separators=(',', ':'))
        enc = execjs.compile(open('./demo.js', 'r', encoding='utf-8').read()).call('encrypt', a)
        json_data = {
            'req': enc
        }
        resp = self.ajax_request(url='https://m.ceair.com/m-base/sale/shopping', json_data=json_data, params={})
        data = resp['data'].get('flights') if resp['data'] else None
        if data:
            self.print_flights(list(self.process_json(data)))
        else:
            print('没有这一天的航班信息!!或者输入了国家')

    def cookie_update(self, html, par: dict):
        """
        处理acw_sc的cookie更新
        :param par: params参数
        :param html: 网页源码
        :return: None
        """
        pattern1 = re.compile(r'.*?arg1=\'(.*?)\';')
        pattern2 = re.compile(r'.*?setCookie\(\"(.*?)\".*?,.*?x\)')
        arg1 = pattern1.findall(html)
        name = pattern2.findall(html)
        if name and arg1:
            print('====开始处理acw_sc_v2====')
            self.cookies[name[0]] = self.acw_sc_v2(arg1[0])
            print('acw_sc_v2 =', self.cookies[name[0]])
            print('====结束处理acw_sc_v2====')
        else:
            item = self.acw_sc_v3(html)
            par.update({
                'u_atoken': item['t'],
                'u_asession': item['csessionid'],
                'u_asig': item['value'],
                'u_aref': '123'
            })
        return par

    @staticmethod
    def acw_sc_v2(arg):
        """
        处理acw_sc_v2
        :param arg: 网页中获取到的实时参数
        :return: acw_sc_v2的生成值
        """
        return execjs.compile(open('./demo.js', 'r', encoding='utf-8').read()).call('getCookie', arg)

    def acw_sc_v3(self, html: str = ''):
        print('====开始处理滑块====')
        if html:
            replace_info(html)
        result = get_226()
        if result['code'] != 0:
            return self.acw_sc_v3()
        print(f'result: {result}')
        print('====结束处理滑块====')
        return result

    @staticmethod
    def process_json(flights):
        for _flight in flights:
            flightNoGroup = _flight['flightNoGroup']
            depTime = _flight['depTime']
            depDate = _flight['depDate']
            depWeek = _flight['depWeek']
            arrTime = _flight['arrTime']
            arrDate = _flight['arrDate']
            arrWeek = _flight['arrWeek']
            depAirportName = _flight['depCityName'] + _flight['depAirportName'] + _flight['depTerminal']
            arrAirportName = _flight['arrCityName'] + _flight['arrAirportName'] + _flight['arrTerminal']
            transferStopInfos = '\n'.join(
                [info['typeText'] + ',' + info['cityName'] + ',' + info['stopTime'] for info in
                 _flight['transferStopInfos']])
            flightServices = '\n'.join(
                [f"{info['flightNoGroup']}, {info['meal']}" for info in _flight['flightServices'] if info])
            fares = '\n'.join(
                [f'{info["baseCabinCodeText"]} : {info["salePrice"]}' for info in _flight['fares'] if info])
            yield {
                'flightNoGroup': flightNoGroup,
                'depDate': depTime + ' ' + depDate + ' ' + depWeek,
                'arrDate': arrTime + ' ' + arrDate + ' ' + arrWeek,
                'depAirportName': depAirportName,
                'arrAirportName': arrAirportName,
                'transferStopInfos': transferStopInfos,
                'flightServices': flightServices,
                'fares': fares
            }

    @staticmethod
    def print_flights(items):
        tb = pt.PrettyTable()
        tb.field_names = ['航班号', '出发时间', '到达时间', '出发机场', '到达机场', '中转信息', '是否含餐食', '价格']
        tb.align = 'c'
        # 填充宽度
        tb.padding_width = 12
        for item in items:
            tb.add_row([item[i] for i in item])
        print(tb)

    @staticmethod
    def get_city_code(city_name):
        """
        获取城市编码
        :param city_name: string
        :return: city code
        """
        while True:
            try:
                json_data = {
                    'methodName': 'searchairport',
                    'IsHighLight': True,
                    'Keyword': city_name,
                    'comeFrom': 'CEAIR_M',
                    'CountryType': None,
                    'salesChannel': '7701',
                    'moduleX': 'mShopping',
                    'os': 'M',
                    'appVersion': '99.0.0',
                    'transactionId': '0520230421151319554',
                }
                headers = {
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
                }
                resp = \
                    requests.post('https://m.ceair.com/m-base/sale/getBasicData', headers=headers,
                                  json=json_data).json()[
                        'data']['Data']['CityList']
                if resp:
                    print(city_name + '---' + resp[0]['CityCode'])
                    return resp[0]['CityCode']
                else:
                    return None
            except KeyError:
                return None
            except:
                time.sleep(2)


if __name__ == '__main__':
    flight = CEAir()
    try:
        while True:
            arr = input('输入到达城市: ')
            dep = input('输入出发城市: ')
            date = input('输入出发时间(20230820): ')
            flight.get_flight(arr=arr, dep=dep, date=date)
    except KeyboardInterrupt:
        print('\n')
        print(flight.cookies)
        print('Bye!')
