from django.urls import path
from .views import *

urlpatterns = [
        path('', home, name='home'),
        path('about/', about, name='about'),
        path('rent/', AdListView.as_view(), name='rent'),
        ]
