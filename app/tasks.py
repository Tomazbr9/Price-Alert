from celery import shared_task

from .scraping import scraping_product_information

from .models import Product, PriceHistory

from decimal import Decimal

from util.email import send_email_for_user

from django.core.exceptions import ObjectDoesNotExist

@shared_task
def check_product_price(product_id: str):
    """
    Função que checa se o produto teve seu preço alterado
    """

    try:
        product: Product = Product.objects.get(pk=product_id)
    except ObjectDoesNotExist:
        return
    
    new_product_information: dict = scraping_product_information(product.url)
    
    product_name: str = new_product_information['name']
    new_price: Decimal = Decimal(str(new_product_information['price']))
    current_price = product.price
    recipient: str = product.user.email

    # Caso o preço for alterado seja para mais caro ou barato é armazenado 
    if new_price != current_price:
        PriceHistory.objects.create(
                    price=new_price,
                    product=product
                )
        product.price = new_price
        product.name = product_name
        product.save()
    
        # Caso o preço seja alterado para mais barato, um email é enviado
        if new_price < current_price:
            send_email_for_user(product_name, new_price, recipient)

@shared_task
def check_price_of_all_products():
    """
    Função que checa os preços de todos os produtos
    """
    products = Product.objects.all()

    for product in products:
        check_product_price.delay(product.pk)