from django.urls import path
from .views import page_detail, send_message
app_name = 'contacts'


urlpatterns = [
    path('', page_detail, name="page"),
    path('send_message', send_message, name="send_message")
]