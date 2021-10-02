from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.CharField(initial=1, widget=forms.NumberInput(attrs={
        'min': 1,
        'max': 99,
        'type': 'number',
        'class': 'quantity__input'
    }))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
