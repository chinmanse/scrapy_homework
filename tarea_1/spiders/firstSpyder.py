import scrapy


class FirstspyderSpider(scrapy.Spider):
    name = "firstSpyder"
    allowed_domains = ["trabajopolis.com"]
    start_urls = ["https://trabajopolis.com"]

    def parse(self, response):
        pass
