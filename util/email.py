from django.core.mail import send_mail
from django.conf import settings
from decimal import Decimal

# Função que envia email ao usuário avisando sobre a mudança de preço
def send_email_for_user(
        name_product: str, 
        new_product_price: Decimal, 
        recipient: str) -> None:

    subject: str = 'Preço Alterado!'
    message: str = f'O preço do produto {name_product} foi alterado para {new_product_price:.2f}!!'

    # Envia o e-mail usando as configurações do projeto
    send_mail(
        subject,
        message, 
        settings.EMAIL_HOST_USER,  # Remetente configurado no settings.py
        [recipient],               # Destinatário
        fail_silently=False        # Se houver erro, ele será lançado
    )
