# -*- coding: utf-8 -*-

from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from items import HPizzaItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
import re

class HPizzaDetailSpider(BaseSpider):
    name = "hpizza_detail"
    allowed_domains = ["www.hardpizza.ru"]
#    start_urls = [
#        "http://www.hardpizza.ru/index.php?option=com_virtuemart&nosef=1&view=productdetails&task=recalculate&virtuemart_product_id=36&format=json&amp;lang=ru&customPrice%255B0%255D%255B11%255D%3D16%26quantity%255B%255D%3D1%26option%3Dcom_virtuemart%26virtuemart_product_id%255B%255D%3D36%26virtuemart_manufacturer_id%3DArray%26virtuemart_category_id%255B%255D%3D9",
#    ]

    def parse(self, response):
        filename = 'fl_detail.txt'
        f = open(filename, 'wb')
        f.write(response.body)
        f.close ()

class HPizzaSpider(CrawlSpider):
    name = "hpizza_common"
    allowed_domains = ["www.hardpizza.ru"]
    start_urls = [
        "http://www.hardpizza.ru/",
#        "http://webcache.googleusercontent.com/search?q=cache:NBh6N9C-FagJ:www.hardpizza.ru/+&cd=1&hl=ru&ct=clnk&gl=ru&client=firefox-a",
    ]
    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(SgmlLinkExtractor(allow=('hardpizza', ),deny=('ru/','guestbook','oplat','component','/pizza/','/dostavka-rollov/','zakazat-rolly')), callback='parse_item', follow=False),
    )
    re_product_id = re.compile ('id=\"productPrice')

    def parse_item (self, response):
        hxs = HtmlXPathSelector(response)
        list_rows = hxs.select('//*[@class="row"]')
        items = []
        value_str = 'value="'
        for rw in list_rows:
            product_split = self.re_product_id.split(rw.extract())
            product_blocks = rw.select ('.//div[@class="spacer"]')
            if len (product_split) > 1:
                for i,product_str in enumerate(product_split[1:]):
                    id = re.split('\"',product_str)[0]
                    nm = product_blocks[i].select('.//h3').extract()[0].replace (u'<h3>\r\n\t\t\t\t\t',u'').replace (u'\t\t\t\t\t\t\t\t\t\t</h3>',u'').strip()
                    size_blocks = product_blocks[i].select('.//div[@class="field_1"]')
                    for sz in size_blocks:
                        sz_extr = sz.extract()
                        p = sz_extr[sz_extr.find(value_str)+len(value_str):]
                        p = p[:p.find('"')]
                        q = sz.select('.//label[@class="other-customfield"]').extract()[0]
                        q = q[q.find('>')+1:]
                        q = q[:q.find('<')].strip()
                        item = HPizzaItem()
                        item['size'] = q
                        item['id'] = id
                        item['name'] = nm
                        item['value'] = p
                        items.append(item)
        for i in items: print i
        filename = 'fl'+response.url.split("/")[-1]+'.html'
        f = open(filename, 'wb')
        f.write(response.body)
        f.close()
        return items

"""        filename = 'fl'+response.url.split("/")[-1]+'.html'
        print '!!!'
        print filename
        open(filename, 'wb').write(response.body) """

