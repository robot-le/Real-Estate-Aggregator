import django_filters as filter
from django import forms
from django_filters.fields import RangeWidget
from .models import *
from django.db.models import Q


class AdFilter(filter.FilterSet):
    site = filter.ChoiceFilter(
            empty_label='Всё сразу',
            choices=(
                ('lalafo.kg', 'lalafo.kg'),
                ('house.kg', 'house.kg'),
                ('doska.kg', 'doska.kg'),
                ),
            widget=forms.Select(attrs={
                'class': 'form-select',
                }),
            )

    category = filter.ChoiceFilter(
            empty_label='Всё сразу',
            choices=(
                ('Дом', 'Дом'),
                ('Квартира', 'Квартира'),
                ('Комната', 'Комната'),
                ),
            widget=forms.Select(attrs={
                'class': 'form-select',
                }),
            )

    # price = filter.RangeFilter(
    #         widget=RangeWidget(attrs={
    #             'class': 'form-control',
    #             }),
    #         )

    price_kgs__gt = filter.NumberFilter(
            field_name='price_kgs',
            lookup_expr='gt',
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'От',
                }),
            )
    
    price_kgs__lt = filter.NumberFilter(
            field_name='price_kgs',
            lookup_expr='lt',
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'До',
                }),
            )

    rooms__gt = filter.NumberFilter(
            field_name='rooms',
            lookup_expr='gt',
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'От',
                }),
            )

    rooms__lt = filter.NumberFilter(
            field_name='rooms',
            lookup_expr='lt',
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'До',
                }),
            )

    search = filter.CharFilter(
            method='search_filter',
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                }),
            )

    def search_filter(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(description__icontains=value) | Q(additional__icontains=value) | Q(address__icontains=value))

    class Meta:
        model = Ad
        fields = [
                'site',
                'category',
                # 'price',
                'rooms',
                ]
