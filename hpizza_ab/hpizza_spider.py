# -*- coding: utf-8 -*-

from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from models import ProductItem, RestoranItem, ProductPortionItem, ProductConnectionItem
import re
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy import log, signals

class HPizzaDetailSpider(BaseSpider):
    name = "hpizza_detail"
    allowed_domains = ["www.hardpizza.ru"]
    findstr = 'salesPrice":"'
    findstr_len = 13

    def __init__(self, portion_item, name=None, **kwargs):
        self.portion_item = portion_item
        super (HPizzaDetailSpider,self).__init__(name, **kwargs)

    def parse(self, response):
        s = response.body[response.body.find(self.findstr)+self.findstr_len:]
        self.portion_item['price'] = s[:s.find('"')].strip()
        if not self.portion_item.save():
            log.msg('Cannot save data. Product - {0}, portion - {1}, value={2}'.format(unicode(self.portion_item['product']),self.portion_item['portion'],self.portion_item['value']),level=log.ERROR,spider=self)

class HPizzaSpider(CrawlSpider):
    name = "hpizza_common"
    allowed_domains = ["www.hardpizza.ru"]
    start_urls = [
        "http://www.hardpizza.ru/",
#        "http://webcache.googleusercontent.com/search?q=cache:NBh6N9C-FagJ:www.hardpizza.ru/+&cd=1&hl=ru&ct=clnk&gl=ru&client=firefox-a",
    ]
    rules = (
        Rule(SgmlLinkExtractor(allow=('hardpizza', ),deny=('ru/','guestbook','oplat','component','/pizza/','/dostavka-rollov/','zakazat-rolly')), callback='parse_item', follow=False),
    )
    re_product_id = re.compile ('id=\"productPrice')

    def __init__(self, restoran_mame='Hard Pizza', *a, **kw):
        restoran_item = RestoranItem()
        restoran_item['restoran_name'] = restoran_mame
        self.restoran_obj = restoran_item.save()
        super (HPizzaSpider,self).__init__(*a, **kw)

    def parse_item (self, response):

        def _chk_signals(spider_name):
            spiders.pop(spider_name)
            if not spiders:
                reactor.stop

        def _create_spider (portion_item,name,wrk_urls):
            spider = HPizzaDetailSpider(portion_item, name=name,start_urls=wrk_urls)
            spiders.append(name)
            crawler = Crawler(Settings({'BOT_NAME':'hpizza_ab','DOWNLOAD_DELAY':4}))
            crawler.signals.connect(lambda x=name: _chk_signals(x), signal=signals.spider_closed)
            crawler.configure()
            crawler.crawl(spider)
            crawler.start()

        hxs = HtmlXPathSelector(response)
        list_rows = hxs.select('//*[@class="row"]')
        spiders = []
        value_str = 'value="'
        for rw in list_rows:
            product_split = self.re_product_id.split(rw.extract())
            product_blocks = rw.select ('.//div[@class="spacer"]')
            if len (product_split) > 1:
                for i,product_str in enumerate(product_split[1:]):
                    product_item = ProductItem()
                    product_item['title'] = product_blocks[i].select('.//h3').extract()[0].replace (u'<h3>\r\n\t\t\t\t\t',u'').replace (u'\t\t\t\t\t\t\t\t\t\t</h3>',u'').strip()
                    product_item['restoran'] = self.restoran_obj
                    product_obj = product_item.read_model_for_key()
                    new_prod = not product_obj
                    if new_prod:
                        product_obj = product_item.save()
                        log.msg('New product "{0}" in restoran {1}'.format(product_item['title'],unicode(self.restoran_obj)),level=log.INFO,spider=self)
                    product_conn_item = ProductConnectionItem()
                    product_conn_item['product'] = product_obj
                    id = re.split('\"',product_str)[0]
                    if not product_conn_item.set_items_for_model():
                        product_conn_item['product_site_id'] = id
                        product_conn_item.save()
                    elif product_conn_item['product_site_id'] != id:
                        s = 'Site ID for product "{0}" in restoran {1} was changed.Old ID is {2}, new ID is {3}'
                        log.msg('Site ID for product "{0}" in restoran {1} was changed.Old ID is {2}, new ID is {3}'.format(
                                product_item['title'],unicode(self.restoran_obj),product_conn_item['product_site_id'],id),
                                level=log.WARNING,spider=self)
                        product_conn_item['product_site_id'] = id
                        product_conn_item.save()
                    size_blocks = product_blocks[i].select('.//div[@class="field_1"]')
                    portion_item = ProductPortionItem()
                    portion_item['product'] = product_obj
                    for sz in size_blocks:
                        sz_extr = sz.extract()
                        p = sz_extr[sz_extr.find(value_str)+len(value_str):]
                        p = p[:p.find('"')]
                        q = sz.select('.//label[@class="other-customfield"]').extract()[0]
                        q = q[q.find('>')+1:]
                        q = q[:q.find('<')].strip()
                        portion_item['portion'] = q
                        portion_item['value'] = p
                        wrk_urls = ["http://www.hardpizza.ru/index.php?option=com_virtuemart&nosef=1&view=productdetails&task=recalculate&virtuemart_product_id="+
                            product_conn_item['product_site_id'].strip()+"&format=json&amp;lang=ru&customPrice%255B0%255D%255B11%255D%3D"+portion_item['value']+
                            "%26quantity%255B%255D%3D1%26option%3Dcom_virtuemart%26virtuemart_product_id%255B%255D%3D"+product_conn_item['product_site_id'].strip()+
                            "%26virtuemart_manufacturer_id%3DArray%26"]
                        p = 'hpizza_detail_'+product_conn_item['product_site_id']+'_'+portion_item['value']
#                        _create_spider (portion_item,p,wrk_urls)
#                    log.start(logfile='details'+id+'.txt',loglevel=log.DEBUG,logstdout=False)
#                    reactor.run()
#                    product_item['price'] = portion_item.get_minimal_price()
                    product_item.save()



"""
spider = HPizzaDetailSpider(start_urls=["http://www.hardpizza.ru/index.php?option=com_virtuemart&nosef=1&view=productdetails&task=recalculate&virtuemart_product_id=36&format=json&amp;lang=ru&customPrice%255B0%255D%255B11%255D%3D16%26quantity%255B%255D%3D1%26option%3Dcom_virtuemart%26virtuemart_product_id%255B%255D%3D36%26virtuemart_manufacturer_id%3DArray%26virtuemart_category_id%255B%255D%3D9",])
crawler = Crawler(Settings({'BOT_NAME':'hpizza_ab','DOWNLOAD_DELAY':4}))
crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
crawler.configure()
crawler.crawl(spider)
crawler.start()
log.start(logfile='crawl.txt',loglevel=log.DEBUG,logstdout=False)
reactor.run() # the script will block here until the spider_closed signal was sent
"""
