from django.contrib import admin
from .models import Section2, Page2


class Section2Inline(admin.TabularInline):
    model = Section2


@admin.register(Page2)
class Page2Admin(admin.ModelAdmin):
    list_display = ['title', ]
    inlines = [Section2Inline]
    prepopulated_fields = {'slug': ('title',)}