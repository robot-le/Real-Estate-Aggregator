from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from ad_scraper import settings as scrapers_settings
from ad_scraper.spiders.lalafo import LalafoSpider


class Command(BaseCommand):
    help = 'Crawling lalafo.kg'

    def handle(self, *args, **options):
        crawler_settings = Settings()
        crawler_settings.setmodule(scrapers_settings)

        process = CrawlerProcess(settings=crawler_settings)

        process.crawl(LalafoSpider)
        process.start()
