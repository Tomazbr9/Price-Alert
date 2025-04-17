from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.urls import reverse

from .forms import ProductForm, RegisterForm, CustomAuthenticationForm

from .models import Product

from .scraping import scraping_product_information

def home(request):

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            scraping = scraping_product_information(product.url)

            product.user = request.user
            product.name = scraping['name']
            product.price = scraping['price']

            product.save()
            form = ProductForm()
    else:
        form = ProductForm()
    
    products = Product.objects.filter(user=request.user) if request.user.is_authenticated else None

    context = {
        'title_page': 'Home',
        'form': form,
        'products': products
    }

    return render(request, 'home.html', context)

def register_view(request):
    form_action = reverse('register')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('login')
    else:
        form = RegisterForm()
    
    context = {
        'form': form,
        'form_action': form_action
    }

    return render(request, 'authentication.html', context)
        

def login_view(request):
    form_action = reverse('login')
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    
    context = {
        'form': form,
        'form_action': form_action
    }

    return render(request, 'authentication.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')