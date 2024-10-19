from django.shortcuts import render
from .models import Product
from .utils import get_offers

def product_list(request):
    productos = Product.objects.all() 
    return render(request, 'scraping/product_list.html', {'productos': productos})

def offer_list(request):
    offers = get_offers()
    return render(request, 'scraping/offer_list.html', {'offers': offers})