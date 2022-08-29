from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from app_shops.models import UserGarbage, ProductProfile, Category, ShopProfile, ProductInShop
from django.core.cache import cache
import random
from django.views.decorators.cache import cache_page  # декоратор кэширования страницы, можно сделать в urls.py
import logging  # для логирования


logger = logging.getLogger(__name__)  # для логирования


def user_basket(username):
    """
    Calculates the quantity of goods and the total cost
    :param username:
    :return: product_count, full_sum
    """
    garbage = UserGarbage.objects.filter(name=username)
    logger.info('Запрошена страница с корзиной пользователя')  # для логирования
    full_sum = 0
    product_count = 0
    for product in garbage:
        full_sum += product.sum
        product_count += product.amount
    return product_count, full_sum


# @cache_page(30)  # указываем время кэширования в секундах
def start_page_context(request):
    """
    Defines information for the user depending on his status
    :param request:
    :return: dict
    """
    start_data_text = dict()
    start_data_text['profile'] = 'n'
    if request.user.is_authenticated:
        try:
            start_data_text['user_profile'] = request.user.profile
            start_data_text['user_status'] = start_data_text['user_profile'].status
            start_data_text['user'] = start_data_text['user_profile'].user
            if start_data_text['user_status'] == 'a':
                start_data_text['user_status_text'] = _('beginner')
            elif start_data_text['user_status'] == 'b':
                start_data_text['user_status_text'] = _('started')
            elif start_data_text['user_status'] == 'c':
                start_data_text['user_status_text'] = _('regular')
            else:
                start_data_text['user_status_text'] = _('constant')
            start_data_text['account_amount'] = _('account amount') + f': {round(request.user.profile.purchases_count, 2)}'
            start_data_text['text_city'] = _('Your city: ') + f'{ start_data_text["user_profile"].city }'
            start_data_text['profile'] = 'y'
        except:
            start_data_text['user'] = request.user
            start_data_text['text_city'] = _(f'Your city is unknown, profile is not completed')
        start_data_text['auth'] = 'y'
        basket_info = user_basket(start_data_text['user'].username)
        start_data_text['basket_product_count'] = basket_info[0]
        start_data_text['basket_full_sum'] = basket_info[1]
        if start_data_text['user'].first_name:
            start_data_text['text_hello'] = _('Welcome to the site, ') + f'{start_data_text["user"].first_name }'
        else:
            start_data_text['text_hello'] = _('Welcome to the site, ') + f'{start_data_text["user"].username}'
        start_data_text['href_out'] = "/users/logout/"
        start_data_text['text_out'] = _('Log off')
        start_data_text['href_edit'] = "/users/another_registration/edit"
        start_data_text['text_edit'] = _('Edit profile')
    else:
        start_data_text['text_hello'] = _('You are not authorized on our website')
        start_data_text['href_login'] = "/users/login/"
        start_data_text['text_login'] = _('Login')
        start_data_text['href_reg_1'] = "/users/registration/"
        start_data_text['text_reg_1'] = _('Simple registration')
        start_data_text['href_reg_2'] = "/users/another_registration/"
        start_data_text['text_reg_2'] = _('Detailed registration')

    return start_data_text


def start_page_context_cache(request):
    if request.user.is_authenticated:
        if request.user not in cache:
            cache.set(request.user, start_page_context(request), 1800)
        data = cache.get(request.user)
    else:
        data = start_page_context(request)
    return data


def start_page(request):
    data = start_page_context_cache(request)
    return render(request, 'market/home.html', context=data)


def contact_page(request):
    data = start_page_context(request)
    return render(request, 'market/contact.html', context=data)
