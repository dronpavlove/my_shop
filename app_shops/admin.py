from django.contrib import admin
from django.db.models import F
from .models import ShopProfile, ProductProfile, Category, ProductInShop, UserGarbage, UserBasket, Promotions
from django.utils.translation import gettext_lazy as _


class ShopProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'city', 'street', 'house_number',
                    'data_of_birth', 'phone', 'email', 'photo', 'purchases_count']
    search_fields = ['name', 'city']  # критерии для поиска
    list_filter = ['city']

    def __str__(self):
        return _('shop profile')


class ProductProfileAdmin(admin.ModelAdmin):
    list_display = ['article', 'name', 'description',
                    'category', 'price', 'amount', 'photo']
    search_fields = ['name', 'category', 'article']  # критерии для поиска
    list_filter = ['category']

    def __str__(self):
        return _('product profile')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon_field']
    search_fields = ['name']  # критерии для поиска

    def __str__(self):
        return _('category')


class PromotionsAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'status']
    search_fields = ['name']  # критерии для поиска
    list_filter = ['status']
    actions = ['mark_as_item_current', 'mark_as_item_inactive']

    def mark_as_item_current(self, request, queryset):  # что делать при выборе действия
        queryset.update(status='y')

    def mark_as_item_inactive(self, request, queryset):
        queryset.update(status='n')

    mark_as_item_current.short_description = 'transfer to status "current"'
    mark_as_item_inactive.short_description = 'transfer to status "inactive"'

    def __str__(self):
        return _('name')


class ProductInShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'in_shop', 'amount', 'article', 'full_description']
    search_fields = ['name']  # критерии для поиска
    list_filter = ['in_shop', 'article']

    def __str__(self):
        return _('product in the store')


class UserGarbageAdmin(admin.ModelAdmin):
    list_display = ['name', 'product', 'shop', 'amount', 'sum']
    search_fields = ['name']  # критерии для поиска
    list_filter = ['name']

    def __str__(self):
        return _('Users Garbage')


class UserBasketAdmin(admin.ModelAdmin):
    list_display = ['user', 'product_name', 'product_photo', 'shop_id', 'product_price', 'amount', 'status', 'creation_data']
    search_fields = ['product_name', 'user']  # критерии для поиска
    list_filter = ['status']
    actions = ['mark_as_item_paid', 'mark_as_item_not_paid', 'mark_as_return_to_store']

    def mark_as_item_paid(self, request, queryset):  # что делать при выборе действия
        queryset.update(status='y')

    def mark_as_item_not_paid(self, request, queryset):
        queryset.update(status='n')

    def mark_as_return_to_store(self, request, queryset):
        for i in queryset:
            name = i.product_name.split(',')[0]
            article = i.product_name.split(' ')[-1]
            if i.status == "n":
                product_to_store = ProductInShop.objects.get(in_shop_id=i.shop_id, name__name=name, name__article=article)
                product_to_store.amount = F('amount') + i.amount  # возвращаем в магазин
                product_to_store.save()
                i.delete()
                #try:
                #    UserBasket.objects.get(user=i.user,
                #                           product_name=i.product_name,
                #                           shop_id=i.shop_id,
                #                           product_price=i.product_price,
                #                           amount=i.amount).delete()
                #except:
                #    pass
    mark_as_item_paid.short_description = _('transfer to status "item paid"')
    mark_as_item_not_paid.short_description = _('transfer to status "item not paid"')
    mark_as_return_to_store.short_description = _('return to store')

    def __str__(self):
        return _('Users Basket')


admin.site.register(ShopProfile, ShopProfileAdmin)
admin.site.register(ProductProfile, ProductProfileAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Promotions, PromotionsAdmin)
admin.site.register(ProductInShop, ProductInShopAdmin)
admin.site.register(UserGarbage, UserGarbageAdmin)
admin.site.register(UserBasket, UserBasketAdmin)
