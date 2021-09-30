from django.contrib import admin
from .models import Category, Product, Kit, Attribute, GalleryImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class KitInline(admin.StackedInline):
    model = Kit


class GalleryImageInline(admin.StackedInline):
    model = GalleryImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [GalleryImageInline, KitInline]

    def save_model(self, request, obj, form, change):
        if obj.price_sale:
            obj.price_current = obj.price_sale
        else:
            obj.price_current = obj.price
        super().save_model(request, obj, form, change)


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
