from django.contrib import admin
from platform_delivery.models import *


@admin.register(Bag)
class BagAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'characteristic', 'quantity', 'value']
    

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'stars']
    

@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
    list_display = ['id']
    
    
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'amount', 'characteristic', 'value']
    
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'client']
    filter_horizontal = ['items']
    
    
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'image']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'product']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'cpf']
    search_fields = ['name', 'cpf']



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0


class CharacteristcInline(admin.TabularInline):
    model = Characteristic
    list_display = ['id', 'product', 'type', 'title', 'quantity']
    extra = 0

@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'category', 'price']
    inlines = [CharacteristcInline, ProductImageInline]

    def price(self, obj):
        return 'R$ %.2f' % obj.value
