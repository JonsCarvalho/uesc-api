# -*- coding: utf-8 -*-
import scrapy


class UescScraperSpider(scrapy.Spider):
    name = 'uesc-scraper'
    # allowed_domains = ['www.uesc.br']
    start_urls = ['http://www.uesc.br/noticias/']

    def parse(self, response):
        data = {}
        news = response.css('table.tabela')
        data['teste']=news.text
        yield data
        # for news_instance in news:
        #     for n in news_instance.css('td.coluna_data_noticia'):
        #         data['date'] = n.css('a').getAll()
        #         yield data

