from . import views
from django.urls import path

app_name = 'information-security'

urlpatterns = [
    path('', views.page, name='page')
]