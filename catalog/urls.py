from . import views
from django.urls import path

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='home'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail')
]