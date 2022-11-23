from django.db import models
from django.contrib.postgres import fields


class Ad(models.Model):
    # site_id = models.ForeignKey(to='Website', on_delete=models.CASCADE)
    # site = models.ForeignKey('Website', on_delete=models.CASCADE)
    site = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    title = models.TextField()
    price_origin = models.DecimalField(max_digits=20, decimal_places=4, null=True)
    price_kgs = models.DecimalField(max_digits=20, decimal_places=4, null=True)
    price_usd = models.DecimalField(max_digits=20, decimal_places=4, null=True)
    usd_rate = models.DecimalField(max_digits=20, decimal_places=4, null=True)
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
    apartment_area = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    land_area = models.DecimalField(max_digits=20, decimal_places=2, null=True)
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


# class Website(models.Model):
#     # id = models.CharField(primary_key=True, max_length=50)
#     name = models.ForeignKey(to=Ad, on_delete=models.CASCADE, primary_key=True)
#     domain = models.URLField(max_length=50)
#
#     # def __str__(self):
#     #     return f'{self.id}'
#
#     class Meta:
#         db_table = 'websites'
