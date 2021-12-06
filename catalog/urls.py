from . import views
from django.urls import path

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='home'),
    path('search/', views.search, name='search'),
    path('question/', views.question, name='question'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('product/<slug:slug>/<str:params>/', views.product_detail_filtered, name='product_detail_filtered'),
    path('product-cat/<slug:slug>/', views.products_by_cat, name='products_by_cat'),
    path('product-cat/<slug:slug>/<str:params>/', views.products_by_attr, name='products_by_attribute')
]