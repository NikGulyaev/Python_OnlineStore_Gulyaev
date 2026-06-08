from django.contrib import admin #type: ignore
from .models import Product, Category

admin.site.register(Product)
admin.site.register(Category)