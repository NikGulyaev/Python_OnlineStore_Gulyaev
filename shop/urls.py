from django.urls import path #type: ignore
from . import views

app_name = 'shop'

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
]
