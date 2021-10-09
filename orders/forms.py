from django import forms
from .models import Order, SHIPPING_CHOICES, CLIENT_TYPES, PAYMENT_CHOICES


class OrderCreateForm(forms.ModelForm):
    full_name = forms.CharField(label='', widget=forms.TextInput(attrs={
        'placeholder': 'ФИО',
        'class': 'checkout-fields__name'
    }))
    client_type = forms.ChoiceField(label='', widget=forms.RadioSelect, choices=CLIENT_TYPES, initial='Физическое лицо')
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'placeholder': 'E-mail',
        'class': 'checkout-fields__email'
    }))
    phone = forms.CharField(label='', widget=forms.TextInput(attrs={
        'placeholder': 'Телефон',
        'class': 'checkout-fields__tel',
        'type': 'tel'
    }))
    address = forms.CharField(label='', widget=forms.TextInput(attrs={
        'placeholder': 'Адрес доставки',
        'class': 'checkout-fields__address'
    }))
    agree = forms.BooleanField(label='Согласен на обработку персональных данных', initial=True)
    comment = forms.CharField(label='', required=False, widget=forms.Textarea(attrs={
        'placeholder': 'Текст'
    }))

    shipping = forms.ChoiceField(label='', widget=forms.RadioSelect, choices=SHIPPING_CHOICES,
                                 initial='Самовывоз со склада в Москве')

    payment = forms.ChoiceField(label='', widget=forms.RadioSelect, choices=PAYMENT_CHOICES,
                                initial='online')

    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'email', 'shipping', 'address', 'comment', 'client_type', 'payment']
