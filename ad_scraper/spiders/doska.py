import scrapy
from ad_scraper.items import HousingItems
from datetime import datetime, timedelta
import re
from ad_scraper.utils import get_usd_rate


usd_rate = get_usd_rate()

class DoskaSpider(scrapy.Spider):
    name = 'doska'
    allowed_domains = ['doska.kg']
    start_urls = [
            'https://doska.kg/cat:118/&type=5&image=1&region=1', # apartments
            'https://doska.kg/cat:120/&type=5&image=1&region=1', # houses
            ]

    def parse(self, response):
        ad_elements = response.xpath('//div[@class="doska_last_items_list"]/*[not(contains(@class, "premium-block"))]')

        for ad_el in ad_elements:
            category = ad_el.xpath('./div[@class="list_full_title"]/div/text()').get().strip()
            upload_time = ad_el.xpath('.//div[@class="list_full_date"]/text()').get().strip()
            url = 'https://doska.kg/' + ad_el.xpath('./div[@class="list_full_title"]/a/@href').get()
            yield scrapy.Request(
                url=url,
                callback=self.parse_ad,
                meta={
                    'category': category,
                    'upload_time': upload_time,
                }
            )

        next_page = response.xpath('//div[@class="elem"]').xpath('./a[contains(text(), "след")]/@href').get()
        if next_page is not None:
            next_url = 'https://doska.kg/' + next_page
            yield scrapy.Request(url=next_url, callback=self.parse)

    def parse_ad(self, response):
        items = HousingItems()
        div_in_col_el = response.xpath('//div[@itemtype="http://schema.org/Place"]/../div')
        items_list = [x for x in response.xpath('//div[@itemtype="http://schema.org/Place"]/div')] + div_in_col_el[1:3]
        items_dict = {key.xpath('.//b/text()').get().strip().replace(':', ''): value.xpath('.//text()').getall()[-1].strip() for (key, value) in dict(zip(items_list, items_list)).items() if not 'этаж' in key.xpath('.//b/text()').get().lower()}

        items['site'] = 'doska.kg'
        items['currency'] = response.xpath('//span[@itemprop="priceCurrency"]/@content').get()
        # items['price'] = response.xpath('//span[@itemprop="price"]/@content').get()
        items['price_origin'] = response.xpath('//span[@itemprop="price"]/@content').get()
        items['price_kgs'] = response.xpath('//span[@itemprop="price"]/@content').get()
        items['usd_rate'] = usd_rate

        if items['currency'] == 'USD' and items['price_origin'] is not None:
            items['price_usd'] = items['price_origin']
            items['price_kgs'] = usd_rate * items['price_origin']
        
        items['description'] = ''.join(response.xpath('//div[@itemtype="http://schema.org/Place"]/../../div[2]/span/text()').getall())
        items['title'] = response.xpath('//h1[@class="item_title"]/text()').getall()[-1].strip()
        items['parse_datetime'] = datetime.now()
        items['ad_url'] = response.url
        items['address'] = items_dict.get('Адрес')
        items['rooms'] = None
        rooms = items_dict.get('Кол - во комнат')
        if rooms is not None and rooms.strip().isdigit():
            items['rooms'] = int(rooms.strip())

        apartment_area = items_dict.get('Общ . площадь')

        if apartment_area is not None:
            items['apartment_area'] = float(apartment_area.replace(' кв . м .', ''))
        else:
            items['apartment_area'] = None

        items['land_area'] = None
        land_area = items_dict.get('Соток')
        if land_area is not None:
            items['land_area'] = float(land_area)
            
        items['series'] = items_dict.get('Серия')
        items['additional'] = items_dict
        items['furniture'] = None
        items['renovation'] = None
        items['pets'] = None
        items['seller'] = items_dict.get('Продавец')

        images_style_attr = response.xpath('//div[contains(@class, "aki_gallery_thumbs")]/div/@style').getall()
        images = []
        for attr in images_style_attr:
            images.append(
                    re.findall(r'url\(.+\)', attr)[0].replace("url('", 'https:').replace('.80.', '.f.').replace("')", "")
                    )

        items['images'] = images

        category = response.meta.get('category')
        if 'квартиры' in category.lower():
            items['category'] = 'Квартира'
        elif 'дома' in category.lower():
            items['category'] = 'Дом'
        else:
            items['category'] = None

        # months = {
        #     ' Января ':   '.01.',
        #     ' Февраля ':  '.02.',
        #     ' Марта ':    '.03.',
        #     ' Апреля ':   '.04.',
        #     ' Мая ':      '.05.',
        #     ' Июня ':     '.06.',
        #     ' Июля ':     '.07.',
        #     ' Августа ':  '.08.',
        #     ' Сентября ': '.09.',
        #     ' Октября ':  '.10.',
        #     ' Ноября ':   '.11.',
        #     ' Декабря ':  '.12.',
        # }
        #
        # upload_time = response.meta.get('upload_time')
        #
        # if 'Позавчера' in upload_time:
        #     date = datetime.now() - timedelta(days=2)
        #     items['upload_time'] = date.strftime('%d.%m.%Y')
        # elif 'Вчера' in upload_time:
        #     date = datetime.now() - timedelta(days=1)
        #     items['upload_time'] = date.strftime('%d.%m.%Y')
        # elif 'Сегодня' in upload_time:
        #     items['upload_time'] = datetime.now().strftime('%d.%m.%Y')
        # else:
        #     for key, value in months.items():
        #         items['upload_time'] = upload_time.replace(key, value)

        yield items
