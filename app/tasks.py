from celery import shared_task

from .scraping import scraping_product_information

from .models import Product

from decimal import Decimal

from util.email import send_email_for_user

@shared_task
def check_product_price(product_id: str):
    product: Product = Product.objects.get(pk=product_id)
    new_product_information: dict = scraping_product_information(product.url)
    
    product_name: str = new_product_information['name']
    product_price: float = new_product_information['price']
    recipient: str = product.user.email

    if product_price != product.price:
        send_email_for_user(product_name, product_price, recipient)
        product.price = Decimal(product_price)
        product.save()

@shared_task
def check_price_of_all_products():
    products = Product.objects.all()

    for product in products:
        check_product_price.delay(product.pk)