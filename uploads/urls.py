from django.urls import path
from .views import products_upload, products_fetch, products_add

app_name = 'uploads'

urlpatterns = [
    path('', products_upload, name='products_upload'),
    path('fetch/', products_fetch, name='fetch'),
    path('add/', products_add, name='add')
]
