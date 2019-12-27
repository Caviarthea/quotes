# -*- coding: utf-8 -*-
import scrapy
from quotes.items import QuotesItem

class QuoteSpider(scrapy.Spider):
    name = 'quote'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.css('.quote')
        for quote in quotes:
            item = QuotesItem()
            item['text'] = quote.css('.text::text').extract_first()
            item['author'] = quote.css('.author::text').extract_first()
            item['tags'] = quote.css('.tags .tag::text').extract()
            yield item
        next = response.css('.paper .next a::attr("href")')
        url = response.urljoin(next)
        yield scrapy.Request(url=url,callback=self.parse)








