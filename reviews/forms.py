from django import forms
from .models import Review, CHOICES


class ReviewForm(forms.ModelForm):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={
        'placeholder': 'Имя'
    }))
    email = forms.CharField(label='', widget=forms.EmailInput(attrs={
        'placeholder': 'E-mail'
    }))
    text = forms.CharField(label='', widget=forms.Textarea(attrs={
        'placeholder': 'Отзыв'
    }))

    class Meta:
        model = Review
        fields = ['rating', 'name', 'email', 'product', 'text']
