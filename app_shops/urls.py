from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from .views import start_shops, ShopListVew, ShopDetailVew, product_detail, \
    CategoryListVew, BasketListVew, check_payment, \
    update_product_list, promotions, product_list
from django.views.decorators.cache import cache_page  # кэширование страницы

urlpatterns = [
    path('', start_shops, name='start_shops'),
    path("shops_list", cache_page(30)(ShopListVew.as_view()), name='shops_list'),
    # path("product_list", product_list_select_related, name='product_list'),
    path("basket", BasketListVew.as_view(), name='basket'),
    path("check", check_payment, name='check'),
    path("promotions", promotions, name="promotions"),
    path("<int:pk>", ShopDetailVew.as_view(), name='shops_detail'),
    path("update_product_list", update_product_list, name='update_product_list'),
    path("<int:pk>/category", CategoryListVew.as_view(), name='category_detail'),
    # path("<int:pk>/category/<int:pk1>", ProductListVew.as_view(), name='product_list'),
    path("<int:pk>/category/<int:pk1>", product_list, name='product_list'),
    path("<int:pk>/category/<int:pk1>/product/<int:pk2>/<str:article>", product_detail, name='product_detail'),
    # re_path(r"<int:pk>/category/<int:pk1>/product/<int:pk2>/(?P<article>\d+)/", product_detail, name='product_detail')
    ]
