from . import views
from django.urls import path

app_name = 'it-services'

urlpatterns = [
    path('', views.page, name='page')
]