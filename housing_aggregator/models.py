from django.db import models
from django.contrib.postgres import fields


class Ad(models.Model):
    site = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    title = models.TextField()
    price = models.DecimalField(max_digits=20, decimal_places=1, null=True)
    currency = models.CharField(max_length=5, null=True)
    description = models.TextField(null=True)
    parse_datetime = models.DateTimeField(
            # auto_now=True,
            )
    ad_url = models.URLField(max_length=400)
    # daily = models.BooleanField(null=True)
    address = models.TextField(null=True)
    additional = models.JSONField()
    images = fields.ArrayField(models.URLField(max_length=400))
    rooms = models.IntegerField(null=True)
    apartment_area = models.IntegerField(null=True)
    land_area = models.IntegerField(null=True)
    series = models.CharField(max_length=50, null=True)
    furniture = models.CharField(max_length=50, null=True)
    renovation = models.CharField(max_length=50, null=True)
    pets = models.CharField(max_length=50, null=True)
    seller = models.CharField(max_length=80, null=True)

    def __str__(self):
        return f'{self.ad_url}'

    class Meta:
        ordering = ['parse_datetime']
        db_table = 'ads'
