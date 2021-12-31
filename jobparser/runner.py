import sys
sys.path.append("..")
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from Lesson_6_Scrapy.jobparser import settings
from Lesson_6_Scrapy.jobparser.spiders.hhru import HhruSpider
from Lesson_6_Scrapy.jobparser.spiders.superjobru import SuperjobruSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhruSpider)
    process.crawl(SuperjobruSpider)

    process.start()
