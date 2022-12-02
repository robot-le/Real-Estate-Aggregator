from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess, Crawler
from scrapy.settings import Settings

from ad_scraper import settings as scrapers_settings
from ad_scraper.spiders.doska import DoskaSpider
from ad_scraper.spiders.house import HouseSpider
from ad_scraper.spiders.lalafo import LalafoSpider


class Command(BaseCommand):
    help = 'Run all scrapers'

    def handle(self, *args, **options):
        settings = Settings()
        settings.setmodule(scrapers_settings)

        process = CrawlerProcess(settings=settings)

        doska_crawler = Crawler(
                DoskaSpider,
                settings=settings,
                )
        house_crawler = Crawler(
                HouseSpider,
                settings=settings,
                )
        lalafo_crawler = Crawler(
                LalafoSpider,
                settings=settings,
                )

        process.crawl(doska_crawler)
        process.crawl(house_crawler)
        process.crawl(lalafo_crawler)
        process.start()
