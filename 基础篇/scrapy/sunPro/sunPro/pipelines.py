# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from itemadapter import ItemAdapter


# class SunproPipeline:
#     def process_item(self, item, spider):
#         # 如何判断item的类型
#         # 将数据写入数据库中，如何保证数据的一致性
#         if item.__class__.__name__ == 'DetailItem':
#             print(item['id'], item['content'])
#         else:
#             print(item['number'], item['title'])
#         return item


class mysqlPipeLine(object):
    # 数据库连接
    conn = None
    cursor = None

    def open_spider(self, spider):
        self.conn = pymysql.Connect(host='127.0.0.1', port=3306, user='root', password='', db='Bossjob', charset='utf8')

    def process_item(self, item, spider):
        self.cursor = self.conn.cursor()

        try:
            self.cursor.execute('insert into new values("%s", "%s", "%s", "%s", "%s", "%s")' %
                                (item['number'], item['title'], item['content'], item['status'], item['city'], item['time']))
            self.conn.commit()
            print('成功插入编号为', item['number'], '的数据!')
        except Exception as e:
            print(e)
            print('error!')
            self.conn.rollback()

        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
