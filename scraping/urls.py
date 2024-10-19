from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.product_list, name='product_list'),
    path('ofertas/', views.offer_list, name='offer_list'),
]