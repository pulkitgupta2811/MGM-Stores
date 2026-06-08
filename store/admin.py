from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Product, Category, Order, OrderItem, CustomUser

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']
    list_editable = ['price']
    search_fields = ['name', 'category__name']
    list_filter = ['category']
    ordering = ['name']
    autocomplete_fields = ['category']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'products_count']
    ordering = ['name']
    search_fields = ['name']
    
    def products_count(self, obj):
        return obj.product_set.count()

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    ordering = ['created_at']
    autocomplete_fields = ['user']
    search_fields = ['user__mobile', 'user__username']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity']
    ordering = ['id']
    autocomplete_fields = ['order', 'product']


admin.site.register(CustomUser, UserAdmin)