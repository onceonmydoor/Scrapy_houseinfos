# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonLinesItemExporter
import pymysql
from twisted.enterprise import adbapi
#专门做数据库处理的模块
from pymysql import cursors

class FangPipeline(object):
    def __init__(self):
        self.newhouse_fp = open('newhouse.json','wb')
        self.esfhouse_fp = open('esfhouse.json','wb')
        self.newhouse_exporter = JsonLinesItemExporter(self.newhouse_fp,ensure_ascii=False)
        self.esfhouse_exporter = JsonLinesItemExporter(self.esfhouse_fp,ensure_ascii=False)

    def process_item(self, item, spider):
        self.newhouse_exporter.export_item(item)
        self.esfhouse_exporter.export_item(item)
        return item
    def close_spider(self,spider):
        self.newhouse_fp.close()
        self.esfhouse_fp.close()


# class FangDBPipeline(object):
#     def __init__(self):
#         dbparams={'host':'127.0.0.1',
#                   'port':3306,
#                   'user': 'root',
#                   'password': 'root',
#                   'charset': 'utf8',
#                   'database': 'newhouse',
#                   'cursorclass': cursors.DictCursor
#         }  # 需要游标类
#         self.conn = pymysql.connect(**dbparams)
#         self.cursor = self.conn.cursor()
#         self._sql = None
#     def process_item(self,item,spider):
#         self.cursor.execute(self.sql,(item['']))
#         return item
#
#     @property
#     def sql(self):
#         if not self._sql:






