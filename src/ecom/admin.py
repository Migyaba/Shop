from django.contrib import admin
from .models import Category, Product



# Revoir l'affichage de la liste des categories et produits
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'date_added')
    prepopulated_fields = {'slug': ('name',)}

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'price', 'date_added')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
