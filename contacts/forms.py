from django import forms


class FeadbackForm(forms.Form):
    name = forms.CharField(label=False, widget=forms.TextInput(attrs={
        'placeholder': 'Ваше имя',
        'class': 'feadback-form__input'
    }))
    tel = forms.CharField(label=False, widget=forms.TextInput(attrs={
        'placeholder': 'Телефон',
        'type': 'tel',
        'class': 'feadback-form__input'
    }))
