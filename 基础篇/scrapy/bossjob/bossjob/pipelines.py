# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class BossjobPipeline:
    def process_item(self, item, spider):
        print(item['detail'])
        return item


class mysqlPipeLine(object):
    # 数据库连接
    conn = None
    cursor = None

    def open_spider(self, spider):
        self.conn = pymysql.Connect(host='127.0.0.1', port=3306, user='root', password='', db='Spider',
                                    charset='utf8')

    def process_item(self, item, spider):
        self.cursor = self.conn.cursor()

        try:
            self.cursor.execute('insert into bossjob values("%s", "%s", "%s", "%s", "%s")' % (
            item["company_name"], item["detail_url"], item["job_name"], item["pay"], item["requirement"]))
            self.conn.commit()
            print('成功插入', item['job_name'], '的工作信息到数据库中!')
        except Exception as e:
            print(e)
            self.conn.rollback()

        return item

    def close_spider(self, spider):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
