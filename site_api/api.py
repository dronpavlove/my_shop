from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, \
    UpdateModelMixin, DestroyModelMixin
from app_shops.models import ShopProfile, Category, Promotions, ProductProfile, ProductInShop
from site_api.serializers import ShopProfileSerializers, UserSerializers, \
    ProductProfileSerializers, CategorySerializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers


class ShopApiList(ListModelMixin, CreateModelMixin, GenericAPIView):
    """
    Представление для получения списка магазинов
    """
    queryset = ShopProfile.objects.all()
    serializer_class = ShopProfileSerializers

    def get(self, request):
        return self.list(request)

    def get_queryset(self):  # фильтрация
        queryset = ShopProfile.objects.all()
        name = self.request.query_params.get('name', 0)
        city = self.request.query_params.get('city', 0)
        if name and city:
            queryset = ShopProfile.objects.filter(name=name, city=city)
        elif name:
            queryset = ShopProfile.objects.filter(name=name)
        elif city:
            queryset = ShopProfile.objects.filter(city=city)
        return queryset

    def post(self, request):
        return self.create(request)


class ShopDetailApi(UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericAPIView):
    """
    Представление для получения детальной информации о магазине,
    а также для его редактирования и удаления
    """
    queryset = ShopProfile.objects.all()
    serializer_class = ShopProfileSerializers

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProductApiList(ListModelMixin, CreateModelMixin, GenericAPIView):
    """
    Представление для получения списка товаров
    """
    queryset = ProductProfile.objects.all()[:50]
    serializer_class = ProductProfileSerializers

    def get(self, request):
        return self.list(request)

    def get_queryset(self):  # фильтрация
        queryset = ProductProfile.objects.all()
        name = self.request.query_params.get('name', 0)
        category = self.request.query_params.get('category', 0)
        if name and category:
            queryset = ProductProfile.objects.filter(name=name, category=category)
        elif name:
            queryset = ProductProfile.objects.filter(name=name)
        elif category:
            queryset = ProductProfile.objects.filter(category=category)
        return queryset

    def post(self, request):
        return self.create(request)


class ProductDetailApi(UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericAPIView):
    """
    Представление для получения детальной информации о товаре,
    а также для его редактирования и удаления
    """
    queryset = ProductProfile.objects.all()
    serializer_class = ProductProfileSerializers

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CategoryApiList(ListModelMixin, CreateModelMixin, GenericAPIView):
    """
    Представление для получения списка магазинов
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializers

    def get(self, request):
        return self.list(request)

    def get_queryset(self):  # фильтрация
        queryset = Category.objects.all()
        name = self.request.query_params.get('name', 0)
        if name:
            queryset = Category.objects.filter(name=name)
        return queryset

    def post(self, request):
        return self.create(request)
