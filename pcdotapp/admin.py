from django.contrib import admin
from .models import ProductType, Category, Product, ProductImage, UserProfile, Cart, Wishlist, Video, ClientLogo,Links

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class VideoInline(admin.TabularInline):
    model = Video
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('heading', 'product_type', 'category', 'original_price', 'discount_price', 'created_at', 'updated_at')
    search_fields = ('heading', 'description')
    list_filter = ('product_type', 'category', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    prepopulated_fields = {'slug': ('heading',)}
    inlines = [ProductImageInline, VideoInline]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type')
    search_fields = ('name',)
    list_filter = ('product_type',)

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity')
    search_fields = ('user__username', 'product__heading')
    list_filter = ('user', 'product')

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    search_fields = ('user__username', 'product__heading')
    list_filter = ('user', 'product')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__username', 'phone_number')
    list_filter = ('user',)


class LinksAdmin(admin.ModelAdmin):
    list_display = ('name', 'website')
    search_fields = ('name',)
    list_filter = ('name',)

admin.site.register(ProductType)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Video)
admin.site.register(ClientLogo)
admin.site.register(Links, LinksAdmin)

