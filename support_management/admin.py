# support_management/admin.py

from django.contrib import admin
from .models import FAQCategory, FAQItem

class FAQItemInline(admin.TabularInline):
    model = FAQItem
    extra = 1

@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    inlines = [FAQItemInline]

@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order')
    list_filter = ('category',)