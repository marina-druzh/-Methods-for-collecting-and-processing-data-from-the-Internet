import scrapy
from scrapy.http import HtmlResponse
from parser_job.items import ParserJobItem


class HhRuSpider(scrapy.Spider):
    name = 'hh_ru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://ufa.hh.ru/search/vacancy?text=python&from=suggest_post&area=99'
                  ]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@data-qa='serp-item__title']/@href").getall()
        for link in links:
            yield response.follow(link, method='GET', callback=self.vacancy_pars)

    def vacancy_pars(self, response: HtmlResponse):
        company_name = response.xpath("//div[contains(@class, 'bloko-column_m-0 bloko-column_l-6')]//span[@data-qa='bloko-header-2']//text()").getall()
        vacancies_name = response.xpath("//h1/text()").get()
        vacansies_salary = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        vacancies_url = response.url
        _id = response.url

        yield ParserJobItem(
            url=vacancies_url,
            name=vacancies_name,
            salary=vacansies_salary,
            company_name=company_name
        )