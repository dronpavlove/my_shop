from __future__ import absolute_import, unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
import logging  # для логирования
import datetime


logger = logging.getLogger(__name__)


class Profile(models.Model):
    """
    User profile model supplementing user information
    """
    STATUS_CHOICES = [
        ('a', _('beginner')),
        ('b', _('started')),
        ('c', _('regular')),
        ('d', _('constant'))
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('user'))
    city = models.CharField(max_length=39, blank=True, verbose_name=_('city'))
    street = models.CharField(max_length=50, blank=True, verbose_name=_('street'))
    postcode = models.IntegerField(verbose_name=_('postcode'), default=0)
    house_number = models.IntegerField(verbose_name=_('house_number'), default=0)
    apartment_number = models.IntegerField(verbose_name=_('apartment_number'), default=0)
    data_of_birth = models.DateField(null=True, blank=True, verbose_name=_('data of birth'))
    phone = models.CharField(null=True, max_length=15, blank=True, verbose_name=_('phone'))
    purchases_count = models.IntegerField(verbose_name=_('account amount'), default=0)
    photo = models.ImageField(upload_to='user_photo', default='default.jpg')
    full_sum_count = models.IntegerField(verbose_name=_('spent'), default=0)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='a', verbose_name=_('status'))

    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('users profile')

    def status_info(self, *args, **kwargs):
        status = self.status
        if self.full_sum_count < 10000:
            self.status = 'a'
        elif self.full_sum_count < 20000:
            self.status = 'b'
        elif self.full_sum_count < 30000:
            self.status = 'c'
        else:
            self.status = 'd'
        if status != self.status:
            logger.info(f'Пользовотель: {self.user}, статус изменён: {self.status}, {datetime}')
        super(Profile, self).save(*args, **kwargs)


    def __str__(self):
        return self.user.username


class UserMessage(models.Model):
    """
    Storage of messages from users
    """
    STATUS_CHOICES = [
        ('y', _('answered')),
        ('n', _('unanswered'))
    ]
    name = models.CharField(max_length=50, blank=True, verbose_name=_('name'))
    email = models.EmailField(null=True, max_length=30, blank=True, verbose_name='email')
    message = models.TextField(max_length=5000, blank=True, verbose_name=_('message'))
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='n', verbose_name=_('status'))

    class Meta:
        verbose_name = _('user message')
        verbose_name_plural = _('users message')

    def __str__(self):
        return self.name
