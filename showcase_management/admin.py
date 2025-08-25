from django.contrib import admin
from django.utils.html import format_html
from .models import NCMChapter, NCMPosition, NCMSubitem, Product, ProductImage

def has_showcase_permission(request):
    """Função auxiliar para verificar a permissão do módulo 'showcase_management'."""
    if request.user.is_superuser:
        return True
    if getattr(request.user, 'user_type', None) == 'LICENSEE' and request.user.is_staff:
        assigned_modules = set()
        for perm in request.user.app_permissions.all():
            assigned_modules.update(perm.get_responsible_modules_list())
        return 'showcase_management' in assigned_modules
    return False

class NCMPositionInline(admin.TabularInline):
    model = NCMPosition
    extra = 1

@admin.register(NCMChapter)
class NCMChapterAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')
    search_fields = ('code', 'description')
    inlines = [NCMPositionInline]
    def has_module_permission(self, request):
        return has_showcase_permission(request)

class NCMSubitemInline(admin.TabularInline):
    model = NCMSubitem
    extra = 1

@admin.register(NCMPosition)
class NCMPositionAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'chapter')
    list_filter = ('chapter',)
    search_fields = ('code', 'description')
    inlines = [NCMSubitemInline]
    def has_module_permission(self, request):
        return has_showcase_permission(request)

@admin.register(NCMSubitem)
class NCMSubitemAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'position')
    list_filter = ('position__chapter',)
    search_fields = ('code', 'description')
    def has_module_permission(self, request):
        return has_showcase_permission(request)

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
    def has_module_permission(self, request):
        return has_showcase_permission(request)

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_thumbnail', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ('product__title',)
    actions = ['approve_images', 'reject_images']
    readonly_fields = ('image_thumbnail',)

    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" style="object-fit: cover; border-radius: 8px;" />', obj.image.url)
        return "Sem imagem"
    image_thumbnail.short_description = 'Pré-visualização'

    def has_module_permission(self, request):
        return has_showcase_permission(request)

    @admin.action(description='Aprovar imagens selecionadas')
    def approve_images(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description='Rejeitar imagens selecionadas')
    def reject_images(self, request, queryset):
        queryset.update(is_approved=False)
