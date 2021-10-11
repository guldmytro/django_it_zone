from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from catalog.sitemaps import ProductSitemap
from blog.sitemaps import ArticleSitemap

sitemaps = {'products': ProductSitemap,
            'posts': ArticleSitemap
            }

urlpatterns = [
    path('cart/', include('cart.urls', namespace='cart')),
    path('checkout/', include('orders.urls', namespace='orders')),
    path('wishlist/', include('wishlist.urls', namespace='wishlist')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('info/', include('pages.urls', namespace='info')),
    path('contacts/', include('contacts.urls', namespace='contacts')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('uploads/', include('uploads.urls', namespace='uploads')),
    path('admin/', admin.site.urls),
    path('', include('catalog.urls', namespace='catalog')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
