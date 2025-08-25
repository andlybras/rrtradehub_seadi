from django.contrib import admin
from .models import NCMChapter, NCMPosition, NCMSubitem, Product, ProductImage

class NCMPositionInline(admin.TabularInline):
    model = NCMPosition
    extra = 1

@admin.register(NCMChapter)
class NCMChapterAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')
    search_fields = ('code', 'description')
    inlines = [NCMPositionInline]

class NCMSubitemInline(admin.TabularInline):
    model = NCMSubitem
    extra = 1

@admin.register(NCMPosition)
class NCMPositionAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'chapter')
    list_filter = ('chapter',)
    search_fields = ('code', 'description')
    inlines = [NCMSubitemInline]

@admin.register(NCMSubitem)
class NCMSubitemAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'position')
    list_filter = ('position__chapter',)
    search_fields = ('code', 'description')

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ('is_approved',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'ncm_subitem', 'is_active')
    list_filter = ('is_active', 'company')
    search_fields = ('title', 'description', 'company__nome_fantasia')
    inlines = [ProductImageInline]

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ('product__title',)
    actions = ['approve_images', 'reject_images']

    @admin.action(description='Aprovar imagens selecionadas')
    def approve_images(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description='Rejeitar imagens selecionadas')
    def reject_images(self, request, queryset):
        queryset.update(is_approved=False)
