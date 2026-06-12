from django import forms #type: ignore
from .models import Customer, Order, Product

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'phone': 'Телефон',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваше имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите вашу фамилию'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@mail.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (999) 999-99-99'
            })
        }
        error_messages = {
            'email': {
                'unique': 'Пользователь с таким email уже существует.'
            }
        }

class OrderForm(forms.Form):
    DELIVERY_CHOICES = [
        ('pickup', 'Самовывоз'),
        ('courier', 'Курьерская доставка'),
        ('post', 'Почта России'),
    ]
    PAYMENT_CHOICES = [
        ('card', 'Банковская карта'),
        ('cash', 'Наличными при получении'),
        ('online', 'Онлайн оплата'),
    ]

    delivery_method = forms.ChoiceField(
        choices=DELIVERY_CHOICES,
        label='Способ доставки',
        widget=forms.RadioSelect(attrs={'class': 'delivery-options'}),
        error_messages={
            'required': 'Пожалуйста, выберите способ доставки.'
        }
    )
    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        label='Способ оплаты',
        widget=forms.RadioSelect(attrs={'class': 'payment-options'}),
        error_messages={
            'required': 'Пожалуйста, выберите способ оплаты.'
        }
    )
    address = forms.CharField(
        max_length=255,
        min_length=10,
        label='Адрес доставки',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Город, улица, дом, квартира'
        }),
        error_messages={
            'required': 'Адрес доставки обязателен.',
            'min_length': 'Адрес должен содержать не менее 10 символов.'
        }
    )
    comments = forms.CharField(
        required=False,
        label='Комментарии к заказу',
        max_length=500,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Особые пожелания, время доставки и т. д.'
        }),
        error_messages={
            'max_length': 'Комментарий не может превышать 500 символов.'
        }
    )

class CartForm(forms.Form):
    product_id = forms.IntegerField(
        label='ID товара',
        widget=forms.HiddenInput()
    )
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        label='Количество',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1'
        })
    )

    def clean_product_id(self):
        product_id = self.cleaned_data['product_id']
        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            raise forms.ValidationError('Товар не найден или недоступен.')
        return product_id
