from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django.utils.translation import gettext_lazy as _


class AuthForm(forms.Form):
    """
    Simple user registration form
    """
    username = forms.CharField()
    password = forms.CharField()  # widget=forms.PasswordInput()


class RegisterForm(UserCreationForm):
    """
    Registration form with additions (standard (first name, last name, email) + city, date of birth)
    """
    first_name = forms.CharField(max_length=30, required=False, help_text=_('name'), label=_('name'))
    last_name = forms.CharField(max_length=30, required=False, help_text=_('last name'), label=_('last name'))
    city = forms.CharField(max_length=39, required=False, help_text=_('city'), label=_('city'))
    street = forms.CharField(max_length=50, required=False, help_text=_('street'), label=_('street'))
    postcode = forms.IntegerField(label=_('postcode'), required=False)
    house_number = forms.IntegerField(label=_('house_number'), required=False)
    apartment_number = forms.IntegerField(label=_('apartment_number'), required=False)
    data_of_birth = forms.DateField(required=True, help_text=_('data of birth'), label=_('data of birth'))
    email = forms.EmailField(max_length=20, required=False, help_text='email')
    phone = forms.CharField(required=False, help_text=_('phone'), label=_('phone'))
    photo = forms.ImageField(label=_('photo'), required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'password1', 'password2', 'city', 'data_of_birth', 'phone', 'photo',
                  'street', 'postcode', 'house_number', 'apartment_number')


# class AddressForm(UserCreationForm):
#     """
#     Форма регистрации с дополнениями
#     """
#     city = forms.CharField(max_length=39, required=False, help_text=_('city'), label=_('city'))
#     street = forms.CharField(max_length=50, required=False, help_text=_('street'), label=_('street'))
#     postcode = forms.IntegerField(label=_('postcode'), required=False)
#     house_number = forms.IntegerField(label=_('house_number'), required=False)
#     apartment_number = forms.IntegerField(label=_('apartment_number'), required=False)

    # class Meta:
    #     model = Profile
    #     fields = ('user.first_name', 'user.last_name',
    #               'city', 'street', 'postcode', 'house_number', 'apartment_number')
