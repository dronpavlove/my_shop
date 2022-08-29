from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db.models import F
from django.views import generic
from market.views import start_page_context, start_page_context_cache
from django.utils.translation import gettext as _
from .models import ShopProfile, ProductInShop, ProductProfile, Category, UserGarbage, UserBasket, Promotions
from .forms import UploadFileForm
from csv import reader
from django.core.cache import cache
import logging  # для логирования
import datetime


logger = logging.getLogger(__name__)


def start_shops(request):
    """
    Generates a list of stores from the model
    :param request:
    :return dict:
    """
    content = start_page_context_cache(request)
    content['shops_list'] = ShopProfile.objects.all()
    return render(request, 'app_shops/shop_list.html', context=content)


def promotions(request):
    """
    Generates a list of stocks from the model
    :param request:
    :return dict:
    """
    content = start_page_context_cache(request)
    cache.get_or_set('promotions_cache', Promotions.objects.filter(status='y'), 60 * 20)
    content['promotions'] = cache.get('promotions_cache')
    return render(request, 'app_shops/promotions.html', context=content)


def check_payment(request):
    """
    Generates a check for payment for selected goods
    :param request:
    :return dict:
    """
    extra_context = start_page_context_cache(request)
    if not 'auth' in extra_context or extra_context['profile'] == 'n':
        response = render(request, 'app_users/userinfo.html', context=extra_context)
        response.status_code = 404
        return response
    try:
        obj = UserGarbage.objects.filter(name=extra_context['user'].username)  # request.user.username)
    except:
        obj = []

    if request.POST:
        obj_list = []
        extra_context['text_pay'] = _('The order has been made. You will be contacted shortly.')
        discount = float(request.POST.get('discount').replace(',', '.'))
        new_sum = round(float(request.POST.get('new_sum').replace(',', '.')), 2)
        flag = 'n'
        extra_context['text_account'] = _('Insufficient funds on the account.')
        # try:
        if extra_context['user_profile'].purchases_count >= new_sum:  # request.user.profile
            flag = 'y'
            extra_context['text_account'] = _('Funds debited from account.')
            extra_context['user_profile'].purchases_count = F('purchases_count') - new_sum
            logger.info(f'Пользовотель: {extra_context["user"]}, списание со счёта: {new_sum}, {datetime}')
            extra_context['user_profile'].full_sum_count = F('full_sum_count') + new_sum
            extra_context['user_profile'].save()
        # except:
        #     pass
        for i in obj:  # объекты из мусорной корзины
            # try:
            product_shop_list = str_in_dict(i.full_description)
            product_info = product_shop_list[0]
            in_shop_info = product_shop_list[1]
            # except:
            #     new_article = str(i.product.name.article) + ',' + str(i.shop_id)
            obj_basket = UserBasket()
            obj_basket.user = extra_context['user_profile']  # user # Profile.objects.get(user=request.user)
            obj_basket.product_name = str(i.product.name.name) + ', ' + str(i.product.name.article)
            obj_basket.product_price = round((i.product.name.price * discount), 2)
            obj_basket.amount = i.amount
            obj_basket.status = flag
            obj_basket.shop_id = i.shop_id
            # try:
            obj_basket.product_photo = product_info['photo']
            # except:
            #     pass
            obj_list.append(obj_basket)
            i.delete()
        logger.info(f'Пользовотель: {extra_context["user"]}, оформил заказ, {datetime}')
        UserBasket.objects.bulk_create(obj_list)
        extra_context['account_amount'] = _('account amount') + f': {extra_context["user_profile"].purchases_count}'
        return render(request, 'app_shops/user_basket_check.html', context=extra_context)


class ShopListVew(generic.ListView):
    """
    Returns objects from the model 'ShopProfile'
    """
    model = ShopProfile  # таблица из моделей
    template_name = 'app_shops/shop_list.html'  # куда будем передавать данные
    context_object_name = 'shops_list'  # как будет называться объект в {%  %}
    queryset = ShopProfile.objects.all()[:20]  # вернёт только 20 объектов [:20]

    def get(self, *args, **kwargs):
        self.extra_context = start_page_context_cache(self.request)
        return super().get(*args, **kwargs)


class ShopDetailVew(generic.DetailView):
    """
    Returns information about a specific object from the model 'ShopProfile'
    """
    model = ShopProfile
    template_name = 'app_shops/shop_detail.html'

    def get(self, *args, **kwargs):
        obj = super().get_object()
        self.extra_context = start_page_context_cache(self.request)
        self.extra_context['photo'] = obj.photo.url
        self.extra_context['href_category'] = f"/shops/{obj.id}/category"
        return super().get(*args, **kwargs)


class CategoryListVew(generic.ListView):
    """
    Returns objects from the model 'Category'
    """
    model = Category
    template_name = 'app_shops/category_detail.html'
    context_object_name = 'category_list'

    def get(self, *args, **kwargs):
        self.extra_context = start_page_context_cache(self.request)
        shop_id = self.request.get_full_path().split('/')[2]
        self.extra_context['shop_name'] = ShopProfile.objects.get(id=shop_id).name
        return super().get(*args, **kwargs)


def product_list(request, *args, **kwargs):
    """
    Returns objects from the model 'ProductInShop'
    """
    context = start_page_context_cache(request)
    if request.method == 'GET':
        shop_id = kwargs['pk']
        category_id = kwargs['pk1']
        obj = ProductInShop.objects.filter(in_shop_id=shop_id, name__category_id=category_id)[:20]
        # TODO посмотрите на этот запрос в debug toolbar, он содержит кроме основного запроса ещё 20 "вспомогательных"
        #  для каждого из 20 товаров. Есть инструмент .select_related() который позволяет всё это сделать одним
        #  запросом, при этом скорость запроса уменьшается более чем в 4 раза.
        context['product_list'] = obj
        return render(request, 'app_shops/product_list.html', context=context)


class BasketListVew(generic.ListView):
    """
    Returns objects from the model 'UserGarbage'
    """
    model = UserGarbage  # таблица из моделей
    template_name = 'app_shops/user_basket.html'  # куда будем передавать данные

    def get(self, *args, **kwargs):
        self.extra_context = start_page_context_cache(self.request)
        try:
            obj = UserGarbage.objects.filter(name=self.extra_context['user'].username)  # self.request.user.username)
        except:
            obj = []
        self.extra_context['product_list'] = obj
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        self.extra_context = start_page_context_cache(self.request)
        try:
            obj = UserGarbage.objects.filter(name=self.extra_context['user'].username)  # self.request.user.username
            values = self.request.POST.getlist('product_basket')
        except:
            obj = []
            values = []
        if not 'auth' in self.extra_context or self.extra_context['profile'] == 'n':
            response = render(self.request, 'app_users/userinfo.html', context=self.extra_context)
            response.status_code = 404
            return response
        self.extra_context['full_sum'] = 0
        self.extra_context['product_list'] = []
        for i in obj:  # список всех желаний пользователя
            try:
                product_shop_list = str_in_dict(i.full_description)
                product_info = product_shop_list[0]
                in_shop_info = product_shop_list[1]
            # new_article = str(i.product.name.article) + ',' + str(i.shop_id)
                new_article = product_info['article'] + ',' + str(in_shop_info['id'])
            except:
                new_article = str(i.product.name.article) + ',' + str(i.shop_id)
            if str(i.product.name) + str(i.shop_id) + str(i.product.name.article) in values:  # если продукт подтвержден это строка КУРТКА1KURT001
                self.extra_context['product_list'].append(i)  # добавляем его в список здесь поправлять надо, совпадающие наименования товаров
                self.extra_context['full_sum'] += float(i.sum)
            else:
                try:
                    product_in_shop = ProductInShop.objects.get(article=new_article)
                    product_in_shop.amount = F('amount') + i.amount  # возвращаем в магазин
                    product_in_shop.save()
                    i.delete()
                except:
                    pass
        self.extra_context['full_sum'] = round(self.extra_context['full_sum'], 2)
        if self.extra_context['user_status'] == 'a':
            self.extra_context['text'] = _('The amount does not allow you to make a discount')
            self.extra_context['discount'] = 1
            self.extra_context['new_sum'] = round(self.extra_context['full_sum'], 2)
        elif self.extra_context['user_status'] == 'b':
            new_sum = round(self.extra_context['full_sum'] * 0.97, 2)
            self.extra_context['text'] = _('You get a 0,03 discount, to pay: ')
            self.extra_context['discount'] = 0.97
            self.extra_context['new_sum'] = new_sum
        elif self.extra_context['user_status'] == 'c':
            new_sum = round(self.extra_context['full_sum'] * 0.93, 2)
            self.extra_context['text'] = _('You get a 0,07 discount, to pay: ')
            self.extra_context['discount'] = 0.93
            self.extra_context['new_sum'] = new_sum
        else:
            new_sum = round(self.extra_context['full_sum'] * 0.9, 2)
            self.extra_context['text'] = _(f'You get a 0,1 discount, to pay: ')
            self.extra_context['discount'] = 0.9
            self.extra_context['new_sum'] = new_sum
        try:
            self.extra_context['user_address'] = self.extra_context['profile'] # Profile.objects.get(user=self.request.user)
        except:
            pass
        return render(self.request, 'app_shops/user_basket_check.html', context=self.extra_context)


def product_detail(request, *args, **kwargs):
    """
    Returns information about a specific object from the model 'ProductInShop'
    """
    context = start_page_context_cache(request)
    shop_id = kwargs['pk']
    category_id = kwargs['pk1']
    article = kwargs['article']
    try:
        context['object'] = ProductInShop.objects.get(article=article)
    except:
        context['object'] = []

    if request.method == 'GET':
        return render(request, 'app_shops/product_detail.html', context=context)

    if request.method == 'POST':
        if context['profile'] == 'y':
            amount = request.POST.get('amount')
            in_shop = context['object']
            if int(amount) > in_shop.amount:
                # context['object'] = in_shop
                context['error'] = _("Order quantity exceeds store stock")
                return render(request, 'app_shops/product_detail.html', context=context)
            else:
                full_sum = in_shop.name.price * int(amount)
                in_shop.amount = F('amount') - amount
                in_shop.save()
                user_name = context['user'].username
                try:
                    in_garbage = UserGarbage.objects.get(product=in_shop, name=user_name, shop_id=shop_id)
                    in_garbage.amount = F('amount') + amount
                    in_garbage.sum = F('sum') + round(full_sum, 2)
                    in_garbage.full_description = in_shop.full_description
                    in_garbage.save()
                except:
                    UserGarbage.objects.create(product=in_shop, name=user_name, amount=amount,
                                               sum=round(full_sum, 2), shop_id=shop_id,
                                               full_description=in_shop.full_description)
                return HttpResponseRedirect(f'/shops/{shop_id}/category/{category_id}')
        else:
            return HttpResponseRedirect('/users')


def update_product_list(request):
    """
    Loading data into the model 'ProductProfile' from a file
    :param request:
    """
    context = start_page_context_cache(request)
    if not 'auth' in context or context['profile'] == 'n':
        response = render(request, 'app_users/userinfo.html', context=context)
        response.status_code = 404
        return response

    elif request.method == 'POST':
        upload_file_form = UploadFileForm(request.POST, request.FILES)
        if upload_file_form.is_valid():
            category_list = [i.name for i in Category.objects.all()]
            product_file = upload_file_form.cleaned_data['file'].read()
            product_str = product_file.decode('1251').split('\n')
            csv_reader = reader(product_str, delimiter=";", quotechar='"')
            for row in csv_reader:
                if len(row) == 7:
                    if len(ProductProfile.objects.filter(article=row[0])) != 0:
                        ProductProfile.objects.filter(article=row[0]).update(
                            name=row[2], description=row[3], price=float(row[4]),
                            amount=int(row[6]))
                    else:
                        if not row[1] in category_list:
                            category_list.append(row[1])
                            new_category = Category()
                            new_category.name = row[1]
                            new_category.save()
                        try:
                            new_product = ProductProfile(article=row[0], category=Category.objects.get(name=row[1]),
                                                         name=row[2], description=row[3],
                                                         price=float(row[4]), photo=row[5],
                                                         amount=int(row[6]))
                            new_product.save()
                        except:
                            pass
            return render(request, 'app_shops/shop_list.html', context=context)
    else:
        upload_file_form = UploadFileForm()
        context = start_page_context(request)
        context['form'] = upload_file_form
        return render(request, 'app_shops/upload_file.html', context=context)


def str_in_dict(text):
    # if "(" in text:
    #     text = text[:text.find("(") - 1:] + text[text.find(")") + 1::]
    new_list = text.split('}{')

    def in_dict(f_list):
        new_data = dict()
        for i in f_list:
            i = i.split(': ')
            new_data[str(i[0])] = str(i[1])
        return new_data

    data_1 = in_dict(new_list[0][2::].replace("'", "").split(', '))
    data_2 = in_dict(new_list[1][:-2:].replace("'", "").split(', '))
    new_list = [data_1, data_2]
    return new_list
