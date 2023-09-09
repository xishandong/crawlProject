import os

from feapder.pipelines import BasePipeline
from feapder.utils.log import log

from RedBook.setting import CSV_PATH
import csv


class CsvPipeline(BasePipeline):
    def __init__(self):
        path = os.path.abspath(os.path.dirname(__file__) + '/csv_data/' + CSV_PATH)
        self.f = open(path, "w", encoding="utf-8", newline='')
        self.len = 0

    def save_items(self, table, items) -> bool:
        try:
            header = list(items[0].keys())
            writer = csv.DictWriter(self.f, header)
            # 如果文件为空，写入表头
            if self.len == 0:
                writer.writeheader()
                self.len = 1
            writer.writerows(items)
            self.f.flush()  # 刷新缓冲区到磁盘
            log.info(f"CSV管道 ===> {table},写入csv文件成功")
            return True
        except Exception as e:
            log.error(f"CSV管道 ===> 错误信息: {e}")
            log.error(f"CSV管道 ===> {table},写入csv文件失败")
            return False

    def close(self):
        self.f.close()
