import scrapy

class FbrefSpider(scrapy.Spider):
    name = "fbref"
    
    def start_requests(self):
        urls = [
            'https://fbref.com/en/comps/9/stats/Premier-League-Stats',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
    def parse(self, response):
        page = response.url.split("/")[-2]