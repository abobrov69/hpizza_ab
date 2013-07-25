from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy import log, signals
from hpizza_spider import HPizzaSpider, HPizzaDetailSpider

spider = HPizzaDetailSpider(121,start_urls=["http://www.hardpizza.ru/index.php?option=com_virtuemart&nosef=1&"+
                                            "view=productdetails&task=recalculate&virtuemart_product_id=36&format=json&amp"+
                                            ";lang=ru&customPrice%255B0%255D%255B11%255D%3D16%26quantity%255B%255D%3D1"+
                                            "%26option%3Dcom_virtuemart%26virtuemart_product_id%255B%255D%3D36"+
                                            "%26virtuemart_manufacturer_id%3DArray%26"])
crawler = Crawler(Settings({'BOT_NAME':'hpizza_ab','DOWNLOAD_DELAY':4}))
#crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
crawler.configure()
crawler.crawl(spider)
crawler.start()
log.start() # (logfile='crawl.txt',loglevel=log.DEBUG,logstdout=False)
reactor.run() # the script will block here until the spider_closed signal was sent