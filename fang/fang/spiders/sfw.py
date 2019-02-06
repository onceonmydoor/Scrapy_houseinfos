# -*- coding: utf-8 -*-
import scrapy
import re
from fang.items import NewHouseItem,ESFHouseItem

class SfwSpider(scrapy.Spider):
    name = 'sfw'
    allowed_domains = ['fang.com']
    start_urls = ['http://www.fang.com/SoufunFamily.htm']

    def parse(self, response):
        trs =response.xpath("//div[@class='outCont']//tr")
        provice =None
        for tr in trs:
            tds =tr.xpath(".//td[not(@class='font01')]")
            provice_td=tds[0]
            provice_text =provice_td.xpath(".//text()").get()
            provice_text =re.sub(r"\s","",provice_text)
            if provice_text:
                provice=provice_text
            #不爬取海外
            if provice =='其它':
                continue
            city_td = tds[1]
            city_links =city_td.xpath(".//a")
            for city_link in city_links:
                city_name = city_link.xpath(".//text()").get()
                city_url = city_link.xpath(".//@href").get()
                # print("省份",provice)
                # print('城市',city_name)
                # print('城市url',city_url)
                url_module =city_url.split(".")
                scheme =url_module[0]
                fang =url_module[1]
                com = url_module[2]
                if 'http://bj' in scheme:
                    newhouse_url="http://newhouse.fang.com/house/s/?from=db"
                    esf_url="http://esf.fang.com/?ctm=1.bj.xf_search.head.105"
                else:
                    #新房url
                    newhouse_url =scheme+'.'+"newhouse."+fang+"."+com+"house/s/"
                    #旧房url
                    esf_url =scheme+'.'+"esf."+fang+"."+com
                yield scrapy.Request(url=newhouse_url,callback=self.parse_newhouse,meta={"info":(provice,city_name)})
                yield scrapy.Request(url=esf_url, callback=self.parse_esf, meta={"info": (provice, city_name)})
    def parse_newhouse(self,response):
        province,city =response.meta.get('info')
        #获取yield中的元组
        lis = response.xpath("//div[contains(@class,'nl_con clearfix')]/ul/li[not(@id)]")
        for li in lis:
            name = "".join(li.xpath(".//div[@class='nlcd_name']/a/text()").get())
            # if name!=None:
            #     name=name.strip()
            #     print(name)
            house_type_list = li.xpath(".//div[contains(@class,'house_type')]/a/text()").getall()
            house_type_list=list(map(lambda x:re.sub(r"\s","",x),house_type_list))
            rooms = list(filter(lambda x:x.endswith("居"),house_type_list))
            #print(rooms)
            area="".join(li.xpath(".//div[contains(@class,'house_type')]/text()").getall())
            area = re.sub(r"\s|－|/","",area)
            #print(area)
            address = li.xpath(".//div[@class = 'address']/a/@title").get()
            #print(address)
            district_text = "".join(li.xpath(".//div[@class ='address']/a//text()").getall())
            try:
                district = re.search(r".*\[(.+)\].*",district_text).group(1)
            except Exception:
                district = ""
            #print(district)
            sale = li.xpath(".//div[contains(@class,'fangyuan')]/span/text()").get()
            #售楼状态是第一个，只需要一个get
            #print(sale)
            price = "".join(li.xpath(".//div[contains(@class,'nhouse_price')]//text()").getall())
            price = re.sub(r"\s|广告","",price)
            #print(price)
            origin_url = "http:"+li.xpath(".//div[@class='nlcd_name']/a/@href").get()
            #print(origin_url)

            item  =NewHouseItem(province=province,city=city,name=name,rooms=rooms,address=address,area=area,district=district,price=price,sale=sale,origin_url=origin_url)
            yield item

        next_url = response.xpath("//div[@class='page']/a[@class='next']/@href").get()
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url),callback=self.parse_newhouse,meta={"info":(provice,city)})



    def parse_esf(self,response):
        province,city =response.meta.get('info')

        #print(name)
        dls = response.xpath("//dl[contains(@dataflag,'bg')]")
        for dl in dls:
            item = ESFHouseItem(province=province,city=city)
            name = ''.join(dl.xpath(".//dd//p[@class='add_shop']/a/@title").getall())
            item['name']=name
            infos = dl.xpath(".//dd//p[@class='tel_shop']//text()").getall()
            infos = list(map(lambda x:re.sub(r"\s|\|",'',x),infos))
            infos = list(filter(None,infos))
            for info in infos:
                if "厅" in info:
                    item['rooms']=info
                elif '层' in info:
                    item['floor']=info
                elif '年' in info:
                    item['year']=info
                elif '向' in info:
                    item['toward']=info
                elif '㎡' in info:
                    item['area']=info
            address = dl.xpath(".//dd//p[@class='add_shop']//span//text()").getall()
            item['address']=address
            price = "".join(dl.xpath(".//dd[@class='price_right']//span[@class='red']//text()").getall())
            item['price'] = price
            unit = "".join(dl.xpath(".//dd[@class='price_right']//span[2]//text()").getall())
            item['unit'] = unit
            detail_url = "".join(dl.xpath(".//h4[@class='clearfix']/a/@href").getall())
            item['origin_url']=response.urljoin(detail_url)
            yield item
        next_url = response.xpath("//div[@class='page_al']//p[1]/a/@href").get()
        yield scrapy.Request(url=response.urljoin(next_url),callback=self.parse_esf,meta={"info":{province,city}})

