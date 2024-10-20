from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, PriceHistory
from django.contrib.auth.decorators import login_required
from .utils import get_offers
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.contrib import messages

def product_list(request):
    productos = Product.objects.all() 
    return render(request, 'scraping/product_list.html', {'productos': productos})

@login_required
def offer_list(request):
    offers = get_offers() 
    
    if request.method == 'POST':
        
        offer_title = request.POST.get('offer_title')
        offer_price = request.POST.get('offer_price')
        offer_url = request.POST.get('offer_url')
        offer_store = request.POST.get('offer_store')
        offer_category = request.POST.get('offer_category')
        
     
        product, created = Product.objects.get_or_create(
            name=offer_title,
            price=offer_price,
            url=offer_url,
            store=offer_store,
            category=offer_category
        )
        

        user = request.user
        if product in user.saved_products.all():
            user.saved_products.remove(product)
        else:
            user.saved_products.add(product)
  
        return redirect('offer_list')

    return render(request, 'scraping/offer_list.html', {'offers': offers})


#productos guardados
def saved_products(request):
    user = request.user
    saved_products = user.saved_products.all() 
    return render(request, 'scraping/product_saved.html', {'saved_products': saved_products})

#vista para usuarios
#registro
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario registrado con éxito. Inicia sesión.')
            return redirect('custom_login')  # Redirige al login
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})



#login
def custom_login(request):
    if request.user.is_authenticated:
        return redirect('offer_list')  # Cambia 'home' por la URL de tu página de inicio

    form = AuthenticationForm(data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, "Inicio de sesión exitoso.")
        return redirect('offer_list')  # Cambia 'home' por la URL a la que quieras redirigir
    else:
        messages.error(request, "Por favor, corrige los errores a continuación.")

    return render(request, 'login/login-user.html', {'form': form})

#logout
class CustomLogoutView(LogoutView):
    next_page = 'login'

@login_required
def save_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    # Si el producto está guardado, lo eliminamos; si no está, lo añadimos
    if product in user.saved_products.all():
        user.saved_products.remove(product)
    else:
        user.saved_products.add(product)

    # Redirigir siempre a la página de productos guardados tras la acción
    return redirect('saved_products')

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    price_history = product.price_history.all().order_by('-date')
    
    context = {
        'product': product,
        'price_history': price_history,
    }
    return render(request, 'product_detail.html', context)