# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class XiaohuaPipeline:
    fp = None

    # 重写父类
    def open_spider(self, spider):
        print('开始爬虫。。。')
        self.fp = open('./xiaohua.txt', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        author = item['author']
        content = item['content']

        # 持久化存储
        self.fp.write(author + '-->' + '\n' + content + '\n')

        return item

    # 重写父类
    def close_spider(self, spider):
        print('结束爬虫！')
        self.fp.close()


class mysqlPipeLine(object):
    # 数据库连接
    conn = None
    cursor = None

    def open_spider(self, spider):
        self.conn = pymysql.Connect(host='127.0.0.1', port=3306, user='root', password='', db='xioahua', charset='utf8')

    def process_item(self, item, spider):
        self.cursor = self.conn.cursor()

        try:
            self.cursor.execute('insert into xiaohua.xiaohua values("%s", "%s")' % (item["author"], item["content"]))
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()