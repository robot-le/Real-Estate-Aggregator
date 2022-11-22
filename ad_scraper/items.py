# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
# from scrapy.contrib.djangoitem import DjangoItem
from housing_aggregator.models import Ad


class HousingItems(DjangoItem):
    django_model = Ad
    
