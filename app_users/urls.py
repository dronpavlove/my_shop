from django.contrib import admin
from django.urls import path, include
from .views import start_users, LoginView, LogoutView, register_view, \
    AnotherRegisterView, UserEditFormViews, purchase_history, \
    login_view, message_view, balance_view, p_h
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', start_users, name='start_users'),  # cache_page(30)
    path('login/', login_view, name='login'),
    path('registration/', register_view, name='registration'),
    path('contact/', message_view, name='message'),
    path('balance/', balance_view, name='balance'),
    path('message/', p_h, name='message'),
    path('purchase_history/', purchase_history, name='purchase_history'),
    path('another_registration/', AnotherRegisterView.as_view(), name='another_registration'),
    path('another_registration/edit/', UserEditFormViews.as_view(), name='another_registration/edit'),
    path('logout/', LogoutView.as_view(), name='logout')
]
