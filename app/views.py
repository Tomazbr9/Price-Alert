from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.urls import reverse

from .forms import ProductForm, RegisterForm, CustomAuthenticationForm

from .models import Product, PriceHistory

from .scraping import scraping_product_information

def home(request):
    """
    View GET ou POST que renderiza a home do projeto ou 
    recebe dados de produtos
    """

    if request.method == 'POST':
        form = ProductForm(request.POST, user=request.user)
        if form.is_valid():
            product = form.save(commit=False)
            scraping = scraping_product_information(product.url)
            
            if request.user.is_authenticated:
                product.user = request.user
                product.name = scraping['name']
                product.price = scraping['price']
                product.save()

                PriceHistory.objects.create(
                    price=product.price,
                    product=product
                )

                form = ProductForm()
            else:
                return redirect('login')
    else:
        form = ProductForm()
    
    products = Product.objects.filter(user=request.user) if request.user.is_authenticated else Product.objects.none()

    context = {
        'title_page': 'Home',
        'form': form,
        'products': products
    }

    return render(request, 'home.html', context)

from .models import Product, PriceHistory

def price_historic_view(request, id):

    """
    View que exibe os historico de preços de cada produto
    """
    product = get_object_or_404(Product, pk=id)
    
    price_history = PriceHistory.objects.filter(product=product).order_by('-date')  # supondo que tenha campo 'date'
    last_price = price_history.first()
    context = {
        'product': product,
        'all_prices': price_history,
        'last_price': last_price
    }

    return render(request, 'price_history.html', context)

def register_view(request):
    """
    View para registro de usuário
    """
    form_action = reverse('register')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('login')
    else:
        form = RegisterForm()
    
    context = {
        'title_page': 'Register',
        'form': form,
        'form_action': form_action,
        'button': 'Cadastrar'
    }

    return render(request, 'authentication.html', context)
        

def login_view(request):
    """
    View para fazer login 
    """
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
        'title_page': 'Login',
        'form': form,
        'form_action': form_action,
        'button': 'Entrar'
    }

    return render(request, 'authentication.html', context)


def logout_view(request):
    """
    View para fazer logout
    """
    logout(request)
    return redirect('login')