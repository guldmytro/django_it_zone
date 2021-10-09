from django.urls import path
from . import views
app_name = 'blog'

urlpatterns = [
    path('', views.archive_blog, name="archive_blog"),
    path('<int:year>/<int:month>/<int:day>/<slug:post>', views.post_detail, name="post_detail"),
]