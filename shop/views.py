from django.shortcuts import render, get_object_or_404, redirect #type: ignore
from django.contrib import messages #type: ignore
from django.contrib.auth import login #type: ignore
from django.contrib.auth.forms import UserCreationForm #type: ignore
from .models import Category, Product, Customer, Order, Cart, CartItem
from .forms import CartForm 

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
    orders = Order.objects.filter(customer=customer).prefetch_related('items__product')
    context = {
        'customer': customer,
        'orders': orders
    }
    return render(request, 'shop/customer_detail.html', context)

# Заказы
def order_list(request):
    orders = Order.objects.select_related('customer').prefetch_related('items__product').all()
    context = {'orders': orders}
    return render(request, 'shop/order_list.html', context)

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {'order': order}
    return render(request, 'shop/order_detail.html', context)

# Корзина
def cart_view(request):
    # Получаем корзину: для авторизованных — по пользователю, для гостей — по сессии
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)

    cart_items = cart.items.select_related('product').all()
    total_price = sum(item.total_price for item in cart_items)

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'shop/cart.html', context)

def add_to_cart(request):
    if request.method == 'POST':
        form = CartForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']

            # Получаем или создаём корзину
            if request.user.is_authenticated:
                cart, created = Cart.objects.get_or_create(user=request.user)
            else:
                session_key = request.session.session_key
                if not session_key:
                    request.session.create()
                    session_key = request.session.session_key
                cart, created = Cart.objects.get_or_create(session_key=session_key)

            # Добавляем товар в корзину
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            messages.success(request, f'{product.name} добавлен в корзину!')
            return redirect('cart')
        else:
            messages.error(request, 'Ошибка в форме. Проверьте корректность данных.')
    else:
        form = CartForm()

    return render(request, 'shop/add_to_cart.html', {'form': form})


#Регистрация
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.Post)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            form = UserCreationForm()
    else:
        form = UserCreationForm()
        return render(request, 'registration/register.html', {'form': form})
