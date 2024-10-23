from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, PriceHistory
from django.contrib.auth.decorators import login_required
from .utils import get_offers
from django.core.paginator import Paginator
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
    # Paginación: dividimos las ofertas en páginas de 20 elementos
    paginator = Paginator(offers, 20)  # 20 ofertas por página
    page_number = request.GET.get('page')  # Obtener el número de página de la URL
    page_offers = paginator.get_page(page_number)  # Obtenemos las ofertas de la página actual

    
    if request.method == 'POST':
        
        offer_title = request.POST.get('offer_title')
        offer_img_url = request.POST.get("img_url")
        offer_price = request.POST.get('offer_price')
        offer_url = request.POST.get('offer_url')
        offer_store = request.POST.get('offer_store')
        offer_category = request.POST.get('offer_category')
        offer_discount = request.POST.get("discount")
        
        offer_price_cleaned = offer_price.replace('.', '').replace(',', '.')
     
        product, created = Product.objects.get_or_create(
            img_url =offer_img_url,
            name=offer_title,
            discount=offer_discount,
            price=offer_price_cleaned,
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

    return render(request, 'scraping/offer_list.html', {'page_offers': page_offers})


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
        return redirect('homepage')  # Cambia 'home' por la URL de tu página de inicio

    form = AuthenticationForm(data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, "Inicio de sesión exitoso.")
        return redirect('homepage')  # Cambia 'home' por la URL a la que quieras redirigir
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

#logica para mostrar ultimos productos guardados del usuario

def group_products(products, n):
  
    for i in range(0, len(products), n):
        yield products[i:i + n]

def homepage(request):
    # Asegurarse de que el usuario esté autenticado
    if request.user.is_authenticated:
        # Obtener los últimos 6 productos guardados por el usuario
        saved_products = Product.objects.filter(saved_by=request.user).order_by('-date_scrapping')[:8]
    else:
        saved_products = []  # Si no está autenticado, devolver una lista vacía

    # Agrupar productos en grupos de 4 para el slider
    grouped_products = list(group_products(saved_products, 4))

    return render(request, 'scraping/homepage.html', {
        'grouped_products': grouped_products,
    })