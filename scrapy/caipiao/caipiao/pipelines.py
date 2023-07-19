# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

'''
存储数据的方案：
    1、数据要存在csv文件中
    2、数据要存在mysql数据库中
    3、数据要存在mongodb数据库中
    4.文件的存储
'''


class CaipiaoPipeline:

    def open_spider(self, spider):
        print('开始存储！')
        self.f = open('./双色球.csv', mode='w', encoding='utf-8')
        self.f.write("期数,红球号码,蓝球号码\n")

    def close_spider(self, spider):
        print('存储完毕！')
        if self.f:
            self.f.close()

    def process_item(self, item, spider):
        # print(item)
        self.f.write(f"{item['qihao']},{' '.join(item['red_ball'])},{item['blue_ball']}\n")
        return item


class mySQLPipeline:

    def open_spider(self, spider):
        print('开始存储！')
        self.conn = pymysql.Connect(
            host="localhost",
            port=3306,
            user="root",
            password="",
            database="spider"
        )

    def close_spider(self, spider):
        print('存储完毕！')
        if self.conn:
            self.conn.close()

    def process_item(self, item, spider):
        cur = self.conn.cursor()
        sql = "insert into caipiao values(%s, %s, %s)"
        try:
            cur.execute(sql, (item['qihao'], item['red_ball'], item['blue_ball']))
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
