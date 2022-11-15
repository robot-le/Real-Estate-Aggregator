from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from .models import Ad

# menu = ['Home', 'Rent', 'FAQs', 'About']

class AdListView(ListView):
    paginate_by = 10
    model = Ad

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['']
    
def home(request):
    return render(request, 'housing_aggregator/home.html')

def faqs(request):
    return render(request, 'housing_aggregator/faqs.html')

def about(request):
    return render(request, 'housing_aggregator/about.html')
