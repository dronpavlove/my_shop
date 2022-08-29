from django.shortcuts import render
from market.views import start_page_context, start_page_context_cache
from django.views import View, generic
from app_shops.models import ProductProfile, UserBasket


class UserBasketSortListVew(generic.ListView):
    """
    Returns sort objects from the model 'UserBasket'
    """
    model = UserBasket  # таблица из моделей
    template_name = 'add_statistics/rating_product_list.html'  # куда будем передавать данные

    def get(self, *args, **kwargs):
        queryset = UserBasket.objects.order_by('amount', 'product_name')
        self.extra_context = self.context_return(queryset)
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        if self.request.POST.get('sort') == "sort_date":
            start_date = self.request.POST.get('start_date')
            fin_date = self.request.POST.get('fin_date')
            product_name = self.request.POST.get('product_name')
            self.extra_context = self.sort_date_queryset(self.request, start_date=start_date, fin_date=fin_date,
                                                         product_name=product_name)
        elif self.request.POST.get('sort') == "sort_1":
            self.extra_context = self.sort_1(self.request)

        elif self.request.POST.get('sort') == "sort_2":
            self.extra_context = self.sort_2(self.request)

        elif self.request.POST.get('sort') == "sort_3":
            self.extra_context = self.sort_3(self.request)

        return super().get(*args, **kwargs)

    def sort_1(self, *args, **kwargs):
        # self.queryset = []
        context = {'func': self.request.POST.get('sort')}
        return context

    def sort_2(self, *args, **kwargs):
        context = {'func': self.request.POST.get('sort')}
        return context

    def sort_3(self, *args, **kwargs):
        context = {'func': self.request.POST.get('sort')}
        return context

    def sort_date_queryset(self, *args, **kwargs):
        queryset = []
        try:
            if (len(kwargs['product_name']) == 0
                    and len(kwargs['start_date']) != 0
                    and len(kwargs['fin_date']) != 0):
                queryset = UserBasket.objects.filter(
                    creation_data__range=[kwargs['start_date'], kwargs['fin_date']])
            elif (len(kwargs['product_name']) != 0
                  and len(kwargs['start_date']) != 0
                  and len(kwargs['fin_date']) != 0):
                queryset = UserBasket.objects.filter(
                    creation_data__range=[kwargs['start_date'], kwargs['fin_date']]
                ).filter(product_name=kwargs['product_name'].title())
        except:
            queryset = UserBasket.objects.order_by('amount', 'product_name')
        return self.context_return(queryset)

    def context_return(self, queryset):
        context = start_page_context_cache(self.request)
        context['product_list'] = {}
        name_product_set = set()
        for product in queryset:
            name_product_set.add(product.product_name)
        for product_name in name_product_set:
            info_product = ProductProfile.objects.get(article=product_name.split(' ')[-1])
            url = info_product.photo.url
            article = info_product.article
            new_queryset = queryset.filter(product_name=product_name, status='y')
            context['product_list'][product_name] = [sum([i.amount for i in new_queryset]), url, article]
        sorted_dict = {}
        sorted_keys = sorted([i[0] for i in context['product_list'].values()])[::-1]
        for w in sorted_keys:
            for key, value in context['product_list'].items():
                if value[0] == w and w != 0:
                    sorted_dict[key] = value
        context['product_list'] = sorted_dict
        return context


class UserBasketListVew(generic.ListView):
    """
    Returns sort objects from the model 'UserBasket'
    """
    queryset = UserBasket.objects.filter(status='y').order_by('-amount')[:5]
    context_object_name = 'product_list'
    template_name = 'add_statistics/product_list.html'
