from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from ad_scraper import settings as scrapers_settings
from ad_scraper.spiders.doska import DoskaSpider


class Command(BaseCommand):
    help = 'Crawling doska.kg'

    def handle(self, *args, **options):
        crawler_settings = Settings()
        crawler_settings.setmodule(scrapers_settings)

        process = CrawlerProcess(settings=crawler_settings)

        process.crawl(DoskaSpider)
        process.start()
