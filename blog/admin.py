from django.contrib import admin
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    search_fields = ['title']
    list_editable = ['status']
    list_filter = ['status', 'created', 'updated']
    prepopulated_fields = {'slug': ('title',)}

