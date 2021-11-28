from . import views
from django.urls import path

app_name = 'brands'

urlpatterns = [
    path('', views.index, name='home'),
    path('<str:str>/', views.filter, name='filter'),
    path('detail/<slug:slug>/', views.detail, name='detail'),
    path('detail/<slug:slug>/<int:paged>/', views.detail_paged, name='detail_paged'),
]