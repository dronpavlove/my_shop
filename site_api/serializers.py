from django.contrib.auth.models import User
from rest_framework import serializers
from app_shops.models import ShopProfile, Category, Promotions, ProductProfile, ProductInShop


class UserSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'is_staff', 'username', 'email']


class ShopProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = ShopProfile
        fields = ['id', 'name', 'description', 'city', 'street', 'house_number', 'data_of_birth',
                  'phone', 'email', 'photo']


class ProductInShopSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductInShop
        fields = ['name', 'in_shop', 'amount']


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon_field']


class ProductProfileSerializers(serializers.ModelSerializer):
    # in_shop = serializers.SerializerMethodField('product_in_shop')
    #
    # def product_in_shop(self, request):
    #     queryset = []
    #     for i in ProductInShop.objects.filter(name_id=request.id):
    #         queryset.append({'shop_id': i.in_shop.id, 'shop_name': i.in_shop.name, 'amount': i.amount})
    #     return queryset

    class Meta:
        model = ProductProfile
        fields = ['id', 'article', 'category', 'name',
                  'description', 'price', 'photo', 'amount']  # , 'in_shop']
