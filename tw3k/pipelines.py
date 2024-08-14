# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pandas as pd
import os


class Tw3KPipeline:
    def open_spider(self, spider):
        self.items = []  # 用于存储每行数据
        self.wkdir = os.path.join(os.getcwd(), 'Data/')
        os.chdir(self.wkdir)

    def process_item(self, item, spider):
        # Transform Customize Item into dict
        adapter = ItemAdapter(item)
        item_dict = adapter.asdict()

        self.items.append(item_dict)

        return item

    def close_spider(self, spider):
        if spider.name == 'character':
            # 创建DataFrame对象
            df = pd.DataFrame(self.items)
            pass
            # 将DataFrame写入Excel文件，并指定sheet_name为"characters"
            with pd.ExcelWriter("tw3k.xlsx", engine='openpyxl', mode='a') as writer:
                df.to_excel(writer, sheet_name=f"{spider.name}_cn", index=False)

        elif spider.name == 'faction':
            df = pd.DataFrame(self.items)
            pass
            with pd.ExcelWriter("tw3k.xlsx", engine='openpyxl', mode='a') as writer:
                df.to_excel(writer, sheet_name=f"{spider.name}_en", index=False)

        else:
            pass
