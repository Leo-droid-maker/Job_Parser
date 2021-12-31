import sys
sys.path.append("..")
import scrapy
from scrapy.http import HtmlResponse
from Lesson_6_Scrapy.jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://spb.hh.ru/search/vacancy?area=2&fromSearchLine=true&text=python']

    def parse(self, response: HtmlResponse):
        # print('HERE ' + response.url)
        next_page_link = response.xpath('//a[@data-qa="pager-next"]/@href').get()
        # next_page = response.xpath('//span[contains(text(),"дальше")]').get()
        if next_page_link:
            yield response.follow(next_page_link, callback=self.parse)
        links = response.xpath('//a[@data-qa="vacancy-serp__vacancy-title"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath('//h1//text()').get()
        salary = response.xpath("//div[@class='vacancy-salary']//text()").getall()
        link = response.url
        item = JobparserItem(name=name, salary=salary, link=link)
        yield item