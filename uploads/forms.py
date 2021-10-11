from django import forms
from django.core import validators
from .models import Csv
from catalog.models import GalleryImage


class CsvForm(forms.ModelForm):
    file = forms.FileField(label='', validators=[validators.FileExtensionValidator(
        allowed_extensions=('csv',))], error_messages={'invalid_extension': 'Этот формат файла не поддерживается'})

    class Meta:
        model = Csv
        fields = ['file']


class ImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = '__all__'

