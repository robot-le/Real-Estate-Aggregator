from datetime import datetime
from ad_scraper.items import HousingItems
import scrapy
import json
from ad_scraper.utils import get_usd_rate


usd_rate = get_usd_rate()

rent_house_id = 2032
rent_apartments_id = 2043
rent_room_id = 2051
bishkek_id = 103184

headers = {
    'accept': 'application/json',
    'accept - encoding': 'gzip, deflate, br',
    'accept - language': 'en-US,en;q=0.8,ru;q=0.9',
    'language': 'ru_RU',
    'device': 'pc',
}


class LalafoSpider(scrapy.Spider):
    name = 'lalafo'
    allowed_domains = ['lalafo.kg']
    start_urls = [
        f'https://lalafo.kg/api/search/v3/feed/search?category_id={rent_house_id}&city_id={bishkek_id}',
        f'https://lalafo.kg/api/search/v3/feed/search?category_id={rent_apartments_id}&city_id={bishkek_id}',
        f'https://lalafo.kg/api/search/v3/feed/search?category_id={rent_room_id}&city_id={bishkek_id}',
        ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                headers=headers,
                callback=self.parse,
            )

    def parse(self, response):
        yield scrapy.Request(
            url=response.url,
            headers=headers,
            callback=self.parse_api,
            dont_filter=True,
        )

    def parse_api(self, response):
        data = json.loads(response.body)
        for item in data['items']:
            id = item.get('id')
            yield scrapy.Request(
                url=f'https://lalafo.kg/api/search/v3/feed/details/{id}',
                callback=self.parse_details,
                headers=headers,
                meta={
                    'ad_label': item.get('ad_label'),
                }
            )

        next_page = data.get('_links').get('next')
        if next_page is not None:
            url = 'https://lalafo.kg/api/search/v3/feed/' + next_page.get('href')[8:]
            yield scrapy.Request(
                url=url,
                callback=self.parse_api,
                headers=headers,
            )

    def parse_details(self, response):
        item = json.loads(response.body)
        items = HousingItems()

        items['site'] = 'lalafo.kg'
        items['title'] = item.get('title')
        items['currency'] = item.get('currency')
        items['price_origin'] = item.get('price')
        items['price_kgs'] = items['price_origin']
        items['usd_rate'] = usd_rate

        if items['currency'] == 'USD' and items['price_origin'] is not None:
            items['price_usd'] = items['price_origin']
            items['price_kgs'] = usd_rate * items['price_origin']

        items['description'] = item.get('description')
        items['parse_datetime'] = datetime.now()
        items['ad_url'] = item.get('url')
        images = item.get('images')
        if images:
            items['images'] = [x['original_url'] for x in images]
        else:
            items['images'] = []

        category = response.meta.get('ad_label')

        if '??????????????' in category.lower():
            items['category'] = '????????????????'
        elif '??????' in category.lower():
            items['category'] = '??????'
        elif '????????????' in category.lower():
            items['category'] = '??????????????'
        else:
            items['category'] = None

        params = item.get('params')
        if params:
            params_dict = {x['name']: x['value'] for x in params}
            items['additional'] = params_dict
        else:
            params_dict = {}
            items['additional'] = None

        items['address'] = params_dict.get('??????????')
        items['rooms'] = None
        rooms = params_dict.get('???????????????????? ????????????')
        if rooms is not None:
            rooms_str = ''.join([x for x in rooms.split() if x.isdigit()])
            if rooms_str != '':
                items['rooms'] = int(rooms_str)

        items['apartment_area'] = params_dict.get('?????????????? (??2)')
        items['land_area'] = params_dict.get('?????????????? ?????????????? (??????????)')
        items['series'] = params_dict.get('??????????')
        items['furniture'] = params_dict.get('????????????')
        items['pets'] = params_dict.get('????????????????')
        items['renovation'] = params_dict.get('????????????')
        items['seller'] = params_dict.get('?????? ??????????')

        yield items
