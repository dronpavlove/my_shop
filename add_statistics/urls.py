from django.urls import path, include
from django.views.decorators.cache import cache_page
from .views import UserBasketSortListVew, UserBasketListVew

urlpatterns = [
    path('rating/', UserBasketSortListVew.as_view(), name='rating'),
    path('full_rating/', UserBasketListVew.as_view(), name='full_rating'),
   ]
