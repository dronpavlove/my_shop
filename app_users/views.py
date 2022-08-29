from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from .forms import RegisterForm
from .models import Profile, UserMessage
from app_shops.models import ProductProfile, ShopProfile, UserBasket
from django.views import View, generic
from django.contrib.auth.models import User
from market.views import start_page_context, start_page_context_cache
from django.utils.translation import gettext as _
import logging  # для логирования
import datetime


logger = logging.getLogger(__name__)


def start_users(request):
    """
    Opens a page with information about user rights
    :param request:
    :return:
    """
    content = start_page_context_cache(request)
    return render(request, 'app_users/userinfo.html', context=content)


def p_h(request):
    extra_context = start_page_context_cache(request)
    if not 'auth' in extra_context or extra_context['profile'] == 'n':
        response = render(request, 'app_users/userinfo.html', context=extra_context)
        response.status_code = 404
        return response
    extra_context['product_list'] = UserMessage.objects.all()
    return render(request, 'app_users/p_h.html', context=extra_context)


def purchase_history(request):
    """
    Generates a list of products from the user's selection history.
    Allows you to pay for unpaid goods.
    :param request:
    :return dict:
    """
    extra_context = start_page_context(request)

    if request.method == 'GET':
        extra_context['product_list'] = []
        if not 'auth' in extra_context or extra_context['profile'] == 'n':
            response = render(request, 'app_users/userinfo.html', context=extra_context)
            response.status_code = 404
            return response
        else:
            try:
                obj = UserBasket.objects.filter(user__user=extra_context['user'])
                extra_context['full_sum'] = obj[0].user.full_sum_count
                for i in obj:
                    m = round(float(i.product_price) * int(i.amount), 2)
                    if i.status == 'y':
                        text = _('paid')
                        pay = 0
                    else:
                        text = _('waiting for payment')
                        pay = 1
                    extra_context['product_list'].append({'id': i.id,
                                                          'product_name': i.product_name,
                                                          'product_price': i.product_price,
                                                          'amount': i.amount,
                                                          'full_count': m,
                                                          'status': text,
                                                          'pay': pay,
                                                          'href': i.product_photo})
            except:
                pass
        return render(request, 'app_users/purchase_history.html', context=extra_context)

    if request.method == 'POST':
        values = request.POST.getlist('product_pay') # product_name, article, amount, id, n
        val = [i.split(",") for i in values]
        obj = UserBasket.objects.filter(user__user=extra_context['user'])
        extra_context['full_sum'] = obj[0].user.full_sum_count
        user_profile = obj[0].user
        balance = obj[0].user.purchases_count
        extra_context['product_list'] = []
        for j in val:
            try:
                prod = obj.get(product_name=j[0] + ',' + j[1], amount=j[2], id=j[3], status=j[4])
                m = round(float(prod.product_price) * int(prod.amount), 2)
                if m <= balance:
                    balance -= m
                    logger.info(f'Пользовотель: {extra_context["user"]}, списание со счёта: {m}, {datetime}')
                    prod.status = 'y'
                    prod.save()
                    extra_context['full_sum'] += m
            except:
                pass
        for i in obj:
            full_count = round(float(i.product_price) * int(i.amount), 2)
            # name = i.product_name.split(',')[0]
            # article = i.product_name.split(' ')[-1]
            if i.status == 'y':
                text = _('paid')
                pay = 0
            else:
                text = _('waiting for payment')
                pay = 1
            extra_context['product_list'].append({'id': i.id,
                                                  'product_name': i.product_name,
                                                  'product_price': i.product_price,
                                                  'amount': i.amount,
                                                  'full_count': full_count,
                                                  'status': text,
                                                  'pay': pay,
                                                  'href': i.product_photo})
            user_profile.purchases_count = round(balance, 2)
            user_profile.full_sum_count = round(extra_context['full_sum'], 2)
            # user_profile.status = user_status(extra_context['full_sum'])
            user_profile.save()
            extra_context['account_amount'] = _('account amount') + f': {user_profile.purchases_count}'

        return render(request, 'app_users/purchase_history.html', context=extra_context)


class AnotherLoginView(LoginView):
    template_name = 'registration/login.html'  # после авторизации LOGIN_REDIRECT_URL = "/"


def login_view(request):
    if request.method == 'POST':  # для POST пытаемся аутентифицировать пользователя
        auth_form = request.POST
        username = auth_form['name']
        password = auth_form['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                logger.info(f'Аутентифицировался: { user.username }, время аутентификации: {datetime}')  # для логирования
                return redirect('/')
        else:
            form = RegisterForm()
            return render(request, 'registration/registration.html',
                          context={'form': form})
    else:
        pass #return redirect('/users')


class AnotherLogoutView(LogoutView):
    next_page = ''  # можно и так перенаправить


class AnotherRegisterView(View):
    """
    Detailed user registration
    """
    def get(self, request):
        form = RegisterForm()
        return render(request, 'registration/registration.html',
                      context={'form': form})

    def post(self, request):
        user = User()
        user_profile = Profile()
        form = RegisterForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save()
            user_profile.user = user
            user_profile.data_of_birth = form.cleaned_data['data_of_birth']
            user_profile.city = form.cleaned_data['city']
            user_profile.phone = form.cleaned_data['phone']
            try:
                user_profile.photo = form.cleaned_data['photo']
            except:
                pass
            user_profile.save()
            username = form.cleaned_data['username']
            raw_password = form.cleaned_data['password1']
            user_login = authenticate(username=username, password=raw_password)
            login(request, user_login)
            return redirect('/')
        else:
            form = RegisterForm()
            return render(request, 'registration/registration.html', {'form': form})


def register_view(request):
    """
    Simple user registration
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registration.html', {'form': form})


class UserEditFormViews(View):
    """
    Edits an authorized user from the database
    """
    def get(self, request):
        data = start_page_context_cache(request)
        if not 'auth' in data:
            response = render(request, 'app_users/userinfo.html', context=data)
            response.status_code = 404
            return response
        user = data['user']  # User.objects.get(username=request.user.username)
        try:
            user_profile = data['user_profile']  # Profile.objects.get(user_id=user.id)
            data = {
                'username': user.username, 'first_name': user.first_name,
                'last_name': user.last_name, 'email': user.email,
                'password1': user.password, 'password2': user.password,
                'city': user_profile.city,
                'street': user_profile.street,
                'postcode': user_profile.postcode,
                'house_number': user_profile.house_number,
                'apartment_number': user_profile.apartment_number,
                'data_of_birth': user_profile.data_of_birth,
                'phone': user_profile.phone,
                'photo': user_profile.photo
            }
        except:
            data = {
                'username': user.username, 'first_name': user.first_name,
                'last_name': user.last_name, 'email': user.email,
                'password1': user.password, 'password2': user.password,
            }
        form = RegisterForm(initial=data)
        return render(request, 'registration/registration.html',
                      context={'form': form})

    def post(self, request):
        user = request.user  # User.objects.get(username=request.user.username)
        photo = None
        try:
            user_profile = user.profile  # Profile.objects.get(user=user)
            photo = user_profile.photo
        except:
            user_profile = Profile()
        form = RegisterForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save()
            user_profile.user = user
            user_profile.data_of_birth = form.cleaned_data.get('data_of_birth')
            user_profile.city = form.cleaned_data.get('city')
            user_profile.phone = form.cleaned_data.get('phone')
            user_profile.street = form.cleaned_data.get('street')
            user_profile.postcode = form.cleaned_data.get('postcode')
            user_profile.house_number = form.cleaned_data.get('house_number')
            user_profile.apartment_number = form.cleaned_data.get('apartment_number')
            if not form.cleaned_data.get('photo'):
                user_profile.photo = photo
            else:
                user_profile.photo = form.cleaned_data.get('photo')
            user_profile.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user_login = authenticate(username=username, password=raw_password)
            login(request, user_login)
            return redirect('/')
        else:
            return render(request, 'registration/registration.html', {'form': form})


def message_view(request):
    """
    Replenishes the model of messages from users
    :param request:
    :return:
    """
    if request.method == 'POST':
        message_form = request.POST
        try:
            name = message_form['name']
            email = message_form['email']
            message = message_form['message']
            new_message = UserMessage(name=name, email=email, message=message)
            new_message.save()
        except:
            pass

    return redirect('/')


def balance_view(request):
    """
    Conditional replenishment of the balance for
    testing without a payment system
    :param request:
    :return:
    """
    data = start_page_context(request)

    if request.method == 'GET':
        if not 'auth' in data:
            response = render(request, 'app_users/userinfo.html', context=data)
            response.status_code = 404
            return response
        user = data['user']  # User.objects.get(username=request.user.username)
        print(data['user_profile'])
        try:
            user_profile = data['user_profile']  # Profile.objects.get(user_id=user.id)
            new_data = {
                'username': user.username, 'first_name': user.first_name,
                'last_name': user.last_name, 'email': user.email,
                'password1': user.password, 'password2': user.password,
                'city': user_profile.city,
                'street': user_profile.street,
                'postcode': user_profile.postcode,
                'house_number': user_profile.house_number,
                'apartment_number': user_profile.apartment_number,
                'data_of_birth': user_profile.data_of_birth,
                'phone': user_profile.phone,
                'photo': user_profile.photo
            }
        except:
            new_data = {
                'username': user.username, 'first_name': user.first_name,
                'last_name': user.last_name, 'email': user.email,
                'password1': user.password, 'password2': user.password,
            }
        return render(request, 'app_users/balance.html',
                      context=new_data)

    if request.method == 'POST':
        message_form = request.POST
        new_sum = int(message_form['sum'])
        data['user_profile'].purchases_count = F('purchases_count') + new_sum
        data['user_profile'].save()
        logger.info(f'Потльзовотель: {data["user"]}, пополнил баланс до: {data["user_profile"].purchases_count}')

    return redirect('/')


def user_status(full_sum):
    """
    Assigns a status to the user depending on the amount of purchases made by him
    :param full_sum:
    :return:
    """
    if full_sum < 10000:
        return 'a'
    elif full_sum < 20000:
        return 'b'
    elif full_sum < 30000:
        return 'c'
    else:
        return 'd'
