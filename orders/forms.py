from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    full_name = forms.CharField(label='', widget=forms.TextInput(attrs={
        'placeholder': 'ФИО'
    }))
    client_type = forms.CharField(label='', widget=forms.RadioSelect())
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'placeholder': 'E-mail'
    }))
    phone = forms.CharField(label='', widget=forms.TextInput(attrs={
        'placeholder': 'Телефон'
    }))

    class Meta:
        model = Order
        fields = ['full_name', 'email', 'address']