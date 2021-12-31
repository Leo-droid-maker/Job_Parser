import sys
sys.path.append("..")
import scrapy
from scrapy.http import HtmlResponse
from Lesson_6_Scrapy.jobparser.items import JobparserItem


class SuperjobruSpider(scrapy.Spider):
    name = 'superjobru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4']

    def parse(self, response: HtmlResponse):
        next_page_link = response.xpath('//a[@rel="next"]/@href').get()
        if next_page_link:
            yield response.follow(next_page_link, callback=self.parse)
        links = response.xpath('//a[contains(@class, "_1UJAN") and contains(@target, "_blank")]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath('//h1[contains(@class, "_3Jn4o")]/text()').get().replace('&nbsp;', '')
        salary = response.xpath('//span[contains(@class, "_2Wp8I _1e6dO _1XzYb _3Jn4o")]//text()').getall()
        link = response.url
        item = JobparserItem(name=name, salary=salary, link=link)
        yield item
