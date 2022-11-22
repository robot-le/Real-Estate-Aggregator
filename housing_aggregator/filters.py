import django_filters as filter
from .models import *


class AdFilter(filter.FilterSet):
    site = filter.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Ad
        fields = ['site']

