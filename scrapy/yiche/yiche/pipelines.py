# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import time

from itemadapter import ItemAdapter


class YichePipeline:
    def process_item(self, item, spider):
        print(item)
        return item


import pymysql


class mysqlPipeLine(object):
    # 数据库连接
    conn = None
    cursor = None

    def open_spider(self, spider):
        self.conn = pymysql.Connect(host='127.0.0.1', port=3306, user='root', password='', db='Spider',
                                    charset='utf8')
        print('开始插入数据')

    def process_item(self, item, spider):
        self.cursor = self.conn.cursor()

        try:
            i = 0
            if item['car_detail'] == '参数配置暂未公开' or item['car_detail'] == '暂无在售车辆':
                self.cursor.execute('insert into cars values("%s", "%s", "%s", "%s", "%s")' % (
                    item["brand"], item['car_name'], item["car_name"] + item['car_name1'], item["car_num"], item['car_detail']))
                self.conn.commit()
                print(item['car_name'])
            else:
                for k in item['car_detail']:
                    v = item['car_name1'][i]
                    i += 1
                    self.cursor.execute('insert into cars values("%s","%s", "%s", "%s", "%s")' % (
                        item["brand"], item['car_name'], item["car_name"] + ' ' + v, item["car_num"], k))
                    self.conn.commit()
                    print(item['car_name'])
        except Exception as e:
            # print(item)
            print(e)
            self.conn.rollback()

        return item

    def close_spider(self, spider):
        print('结束插入数据')
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
