from django.shortcuts import render, get_object_or_404 #type: ignore
from .models import Category, Product, Customer, Order

# Категории
def category_list(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'shop/category_list.html', context)

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'shop/category_detail.html', context)

# Товары
def product_list(request):
    products = Product.objects.select_related('category').all()
    context = {'products': products}
    return render(request, 'shop/product_list.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {'product': product}
    return render(request, 'shop/product_detail.html', context)

# Клиенты
def customer_list(request):
    customers = Customer.objects.all()
    context = {'customers': customers}
    return render(request, 'shop/customer_list.html', context)

def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    orders = Order.objects.filter(customer=customer).select_related('product')
    context = {
        'customer': customer,
        'orders': orders
    }
    return render(request, 'shop/customer_detail.html', context)

# Заказы
def order_list(request):
    orders = Order.objects.select_related('customer', 'product').all()
    context = {'orders': orders}
    return render(request, 'shop/order_list.html', context)

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {'order': order}
    return render(request, 'shop/order_detail.html', context)
