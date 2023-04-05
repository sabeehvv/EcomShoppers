from django.contrib import admin

# Register your models here.
from csv import list_dialects


from .models import *




admin.site.register(Category)

class ProductImageAdmin(admin.StackedInline): 
    model =ProductImage

class productsizevariant(admin.StackedInline):
    model = SizeVariant

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name' , 'price' ]
    inlines = [ProductImageAdmin , productsizevariant]


@admin.register(ColorVariant)
class ColorVariantAdmin(admin.ModelAdmin):
    list_display = ['color_name' , 'price']
    model = ColorVariant

# @admin.register(SizeVariant)
# class SizeVariantAdmin(admin.ModelAdmin):
#     list_display = ['size_name' , 'price']

#     model = SizeVariant


admin.site.register(Product ,ProductAdmin)


admin.site.register(ProductImage)

admin.site.register(SizeVariant)