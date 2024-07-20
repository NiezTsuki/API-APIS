from rest_framework import generics
from .models import Product, Price
from .serializers import ProductSerializer, PriceSerializer
from django.http import JsonResponse
from django.shortcuts import render, redirect
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm

class ProductListCreate(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class PriceListCreate(generics.ListCreateAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer

class PriceRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer

def product_list_json(request):
    products = Product.objects.all()
    data = []
    for product in products:
        product_data = {
            'Código del producto': product.product_code,
            'Marca': product.brand,
            'Código': product.code,
            'Nombre': product.name,
            'Precio': [
                {'Fecha': price.date, 'Valor': price.value}
                for price in product.prices.all()
            ],
            'Stock': product.stock
        }
        data.append(product_data)
    return JsonResponse(data, safe=False)

def product_list_page(request):
    return render(request, 'product_list.html')

def update_usd_prices(request):
    url = 'https://www.mindicador.cl/api/dolar'
    try:
        response = requests.get(url)
        data = response.json()

        if 'serie' in data and len(data['serie']) > 0 and 'valor' in data['serie'][0]:
            usd_value = data['serie'][0]['valor']
            fecha = data['serie'][0]['fecha']
            return JsonResponse({'status': 'success', 'fecha': fecha, 'valor': usd_value})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to fetch USD price - Invalid response format'})

    except requests.exceptions.RequestException as e:
        return JsonResponse({'status': 'error', 'message': f'Failed to fetch USD price - {str(e)}'})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Tu cuenta ha sido creada! Ahora puedes iniciar sesión')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('product-list-page')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def cart_view(request):
    return render(request, 'product_list.html')
