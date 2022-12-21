from django.contrib import admin
from .models import Product,Images,Allergy,MetaData

# Register your models here.

class ProductMetaDataInline(admin.TabularInline):
    model = MetaData
    extra = 1

class ProductAllergyInline(admin.TabularInline):
    model = Allergy
    extra = 1

class ImageInline(admin.TabularInline):
    model = Images

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','sales_rate')

    inlines = [ImageInline,ProductAllergyInline,ProductMetaDataInline]

admin.site.register(Product,ProductAdmin)