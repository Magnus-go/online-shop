from django.contrib import admin
from .models import Product, Category, Subcategory, Comment


class InlineProductAdmin(admin.TabularInline):
    model = Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_title',)
    prepopulated_fields = {'slug': ('category_title',)}
    inlines = [InlineProductAdmin]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'available')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('category_title', 'parent_category')
    prepopulated_fields = {'slug': ('category_title',)}


admin.site.register(Comment)
