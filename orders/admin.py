from django.contrib import admin
from .models import Order, OrderItem, ApiToken


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'address', 'paid', 'created', 'updated']
    list_display_links = ['id', 'full_name']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]


@admin.register(ApiToken)
class ApiTokenAdmin(admin.ModelAdmin):
    list_display = ['token']

