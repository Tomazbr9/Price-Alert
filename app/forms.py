from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Product

from django import forms
from django.core.exceptions import ValidationError


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['url']
        widgets = {
            'url': forms.URLInput(attrs={
                'placeholder': 'Copie a URL do Produto',
                'class': 'form-control',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_url(self):
        url = self.cleaned_data.get('url')
        if self.user and Product.objects.filter(user=self.user, url=url).exists():
            raise ValidationError('Já existe um produto com essa URL.', code='invalid')
        return url


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Username',
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email',
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Senha',
            'class': 'form-control'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirme a senha',
            'class': 'form-control'
        })

    def clean_email(self):
            email = self.cleaned_data.get('email')

            if User.objects.filter(email=email).exists():
                 self.add_error(
                      'email',
                      ValidationError('Já existe este e-mail', code='invalid')
                 )
            return email

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Adiciona classes Bootstrap nos campos
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nome de usuário',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Senha',
        })