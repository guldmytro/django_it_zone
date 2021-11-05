from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_create, name='checkout'),
    path('pay/<int:id>/', views.order_pay, name='pay'),
    path('pay/complete/', views.order_complete, name='complete'),
]