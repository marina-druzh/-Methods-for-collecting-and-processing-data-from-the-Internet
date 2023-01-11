import scrapy
from scrapy.http import HtmlResponse
from parser_job.items import ParserJobItem


class RabotaRuSpider(scrapy.Spider):
    name = 'rabota_ru'
    allowed_domains = ['rabota.ru']
    page = 1
    urls = 'https://ufa.rabota.ru/vacancy/?query=Developer%20python&sort=relevance&page='
    start_urls = [f"{urls}{page}"]

    def parse(self, response):
        page = response.xpath("//a[@class='pagination-list__last-btn']/@href").get()
        if page:
            next_page = RabotaRuSpider.start_urls[0][0:-1] + page[-1]
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//h3[@class='vacancy-preview-card__title']/a/@href").getall()
        for link in links:
            # print()
            yield response.follow(link, callback=self.vacancy_pars)


    def vacancy_pars(self, response: HtmlResponse):
        company_name = response.xpath("//a[@rel='noopener noreferrer']/text()").get()
        vacancies_name = response.xpath("//h1/text()").get()
        vacansies_salary = response.xpath("//h3[@itemprop]/text()").getall()
        vacancies_url = response.url
        _id = response.url

        yield ParserJobItem(
            url=vacancies_url,
            name=vacancies_name,
            salary=vacansies_salary,
            company_name=company_name)
           