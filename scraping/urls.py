from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

class CustomLogoutView(auth_views.LogoutView):
    next_page = 'login'  

urlpatterns = [
    path('productos/', views.product_list, name='product_list'),
    path('ofertas/', views.offer_list, name='offer_list'),
    path('registro/', views.register, name='register'),
    path('cuenta/', include('django.contrib.auth.urls')),
    path('login/', views.custom_login, name='custom_login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]