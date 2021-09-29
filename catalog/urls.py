from . import views
from django.urls import path

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='home'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('product_cat/<slug:slug>/', views.products_by_cat, name='products_by_cat')
]