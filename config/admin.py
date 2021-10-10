from django.contrib import admin
from .models import Config, Brand


class BrandInline(admin.StackedInline):
    model = Brand


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ['title']
    inlines = [BrandInline]
