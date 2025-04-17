from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    
    # Authentication urls
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout')
]
