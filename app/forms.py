from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Product

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

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True, min_length=3)
    last_name = forms.CharField(required=True, min_length=3)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2'
        ]

    def clean_email(self):
            email = self.cleaned_data.get('email')

            if User.objects.filter(email=email).exists():
                 self.add_error(
                      'email',
                      ValidationError('Já existe este e-mail', code='invalid')
                 )
            return email
    
    def clean_username(self):
            username = self.cleaned_data.get('username')

            if User.objects.filter(username=username).exists():
                 self.add_error(
                      'username',
                      ValidationError('Já existe este nome de usuário', code='invalid')
                 )
            return username