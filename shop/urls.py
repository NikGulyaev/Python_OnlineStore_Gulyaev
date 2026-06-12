from django.urls import path #type: ignore
from . import views

app_name = 'shop'

urlpatterns = [
    # Главная страница магазина
    path('', views.product_list, name='home'),

    # Категории
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:category_id>/', views.category_detail, name='category_detail'),

    # Товары
    path('products/', views.product_list, name='product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),

    # Клиенты
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/<int:customer_id>/', views.customer_detail, name='customer_detail'),

    # Заказы
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),

    # Корзина
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),

    #Регистрация
    path('register/', views.register, name='register'),
]
