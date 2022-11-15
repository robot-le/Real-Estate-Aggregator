from django.db import models


class Ad(models.Model):
    site = models.TextField()
    category = models.CharField(max_length=50)
    title = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    currency = models.CharField(max_length=5, null=True)
    description = models.TextField(null=True)
    parse_datetime = models.DateTimeField()
    ad_url = models.TextField()
    daily = models.BooleanField()
    address = models.TextField(null=True)
    additional = models.TextField(null=True)
    images = models.TextField()

    def __str__(self):
        return f'{self.ad_url}'

    class Meta:
        ordering = ['parse_datetime']
