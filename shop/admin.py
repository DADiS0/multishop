from django.contrib import admin

from .models import Product, Ptype, Brand, Categories

def Slug(instance):
    ptype = instance.ptype
    brand = instance.brand
    return f'{ptype.name},{brand.name}','name'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'price', 'offer', 'ptype','brand']
    list_filter = [ 'price', 'offer', 'ptype','brand']
    search_fields = [ 'name', 'price', 'offer', 'ptype','brand']
    prepopulated_fields = {'slug': ('ptype','brand','name',)}
    date_hierarchy = 'publish'
    ordering = ['publish']

@admin.register(Ptype)
class PtypeAdmin(admin.ModelAdmin):
    list_display = [ 'name','categories']
    list_filter = ['name','categories']
    search_fields = ['name','categories']

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = [ 'name']
    list_filter = ['name']
    search_fields = ['name']   
@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = [ 'name']
    list_filter = ['name']
    search_fields = ['name']   