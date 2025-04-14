from django.contrib import admin

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price']