# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewHouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #省份
    province = scrapy.Field()
    #城市
    city = scrapy.Field()
    #小区名
    name = scrapy.Field()
    #价格
    price = scrapy.Field()
    #X居，列表
    rooms = scrapy.Field()
    #面积
    area = scrapy.Field()
    #地址
    address = scrapy.Field()
    #行政区
    district = scrapy.Field()
    #是否在售
    sale = scrapy.Field()
    #房天下详情页面url
    origin_url = scrapy.Field()


class ESFHouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 省份
    province = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 小区名
    name = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 几室几厅
    rooms = scrapy.Field()
    # 层
    floor = scrapy.Field()
    # 朝向
    toward = scrapy.Field()
    # 年份
    year = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 地址
    address = scrapy.Field()
    #单价
    unit = scrapy.Field()
    # #联系人
    # people = scrapy.Field()
    # 房天下详情页面url
    origin_url = scrapy.Field()



