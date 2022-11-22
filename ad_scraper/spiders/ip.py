import scrapy


class IpSpider(scrapy.Spider):
    name = 'ip'
    allowed_domains = ['myip.com']
    start_urls = ['https://www.myip.com/']

    def parse(self, response):
        for i in range(30):
            yield scrapy.Request(url=self.start_urls[0], callback=self.parse_ip, dont_filter=True)

    def parse_ip(self, response):
        ip = response.xpath('//div[@class="texto_1"]/span/text()').get()
        yield {
                'ip': ip,
                'user-agent': response.request.headers['user-agent'],
            }
