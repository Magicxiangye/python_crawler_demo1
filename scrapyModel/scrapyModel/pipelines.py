# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScrapymodelPipeline:
    def process_item(self, item, spider):
        return item


# 英镑兑换人民币
class PriceConvertPipline(object):
    # 汇率
    exchange_rate = 8.8345

    # 默认要定义的处理方法
    def process_item(self, item, spider):
        # 提取 item 的 price 字段(如￡53.74)
        # 去掉前面英镑符号￡，转换为 float 类型，乘以汇率
        price = float(item['price'][1:]) * self.exchange_rate
        # 保留两位小数返回
        item['price'] = '￥%.2f' %price

        return price
