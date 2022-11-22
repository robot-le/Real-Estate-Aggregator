from itemadapter import ItemAdapter
import psycopg2
from dotenv import load_dotenv
import os

from scrapy.exceptions import DropItem

load_dotenv()

table_name = 'ads'

class DjangoAdPipeline:

    def __init__(self):
        hostname = os.environ.get('HOSTNAME')
        username = os.environ.get('USERNAME')
        password = os.environ.get('PASSWORD')
        database = os.environ.get('DATABASE')

        self.connection = psycopg2.connect(
                        host=hostname,
                        user=username,
                        password=password,
                        dbname=database,
                        )

        self.cur = self.connection.cursor()

    def process_item(self, item, spider):
        
        adapter = ItemAdapter(item)

        self.cur.execute(f"select * from {table_name} where ad_url = (%s)", (adapter['ad_url'], ))

        if self.cur.fetchone() is not None:
            raise DropItem(f"Duplicate item found: {item!r}")

        item.save()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()


class AdsPipeline:
    pass
