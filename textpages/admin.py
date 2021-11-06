from django.contrib import admin
from .models import Section, Page


class SectionInline(admin.TabularInline):
    model = Section


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', ]
    inlines = [SectionInline]
    prepopulated_fields = {'slug': ('title',)}
