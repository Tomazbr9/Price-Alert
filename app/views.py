from django.shortcuts import render
from .forms import ProductForm
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

    context = {
        'title_page': 'Home',
        'form': form,
        'products': Product.objects.filter(user=request.user)
    }

    return render(request, 'home.html', context)

def register(request):
    ...

def login(request):
    ...