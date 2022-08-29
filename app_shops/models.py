from __future__ import absolute_import, unicode_literals
from django.db import models
from django.utils.translation import gettext_lazy as _
from app_users.models import Profile
from django.db.models import F


class ShopProfile(models.Model):
    """
    Store profile model. Contains fields with full information about the store.
    """
    name = models.CharField(max_length=39, blank=True, verbose_name=_('name'))
    description = models.TextField(max_length=500, blank=True, verbose_name=_('description'))
    city = models.CharField(max_length=39, blank=True, verbose_name=_('city'))
    street = models.CharField(max_length=50, blank=True, verbose_name=_('street'))
    house_number = models.IntegerField(verbose_name=_('house number'), default=0)
    data_of_birth = models.DateField(null=True, blank=True, verbose_name=_('date of formation'))
    phone = models.CharField(null=True, max_length=15, blank=True, verbose_name=_('phone'))
    email = models.EmailField(null=True, max_length=30, blank=True, verbose_name='email')
    purchases_count = models.IntegerField(verbose_name=_('number of purchases'), default=0)
    photo = models.ImageField(upload_to='shop_photo', default='default.jpg')

    class Meta:
        verbose_name = _('shop profile')
        verbose_name_plural = _('shops profile')

    def __str__(self):
        return self.name


class Category(models.Model):
    """ Category of products """
    name = models.CharField(max_length=250, verbose_name=_('category name'))
    icon_field = models.ImageField(upload_to='category_icon', default='default.jpg', verbose_name=_('photo'))

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name


class Promotions(models.Model):
    """ Promotions held by stores or website"""
    STATUS_CHOICES = [
        ('y', _('current')),
        ('n', _('inactive'))
    ]
    name = models.CharField(max_length=250, verbose_name=_('promotion name'))
    description = models.TextField(max_length=5000, blank=True, verbose_name=_('description'))
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='y', verbose_name=_('status'))

    class Meta:
        verbose_name = _('promotion')
        verbose_name_plural = _('promotions')

    def __str__(self):
        return self.name


class ProductProfile(models.Model):
    """
    Product profile. Describes the characteristics of the product (price, quantity, value)
    """
    article = models.CharField(max_length=25, default='NOTARTICLE', blank=True, verbose_name=_('article'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=39, blank=True, verbose_name=_('name'))
    description = models.TextField(max_length=500, blank=True, verbose_name=_('description'))
    price = models.FloatField(verbose_name=_('price'), default=0)
    photo = models.ImageField(upload_to='product_photo', default='default.jpg', verbose_name=_('photo'))
    amount = models.IntegerField(verbose_name=_('amount'), default=0)

    class Meta:
        verbose_name = _('product profile')
        verbose_name_plural = _('products profile')

    def __str__(self):
        return self.name


class ProductInShop(models.Model):
    """
    Model of distribution of products in stores.
    Automatically subtracts the quantity of a specific
    item from the quantity of the item in stock.
    """
    name = models.ForeignKey(ProductProfile, on_delete=models.CASCADE, verbose_name=_('name'))
    in_shop = models.ForeignKey(ShopProfile, on_delete=models.CASCADE, verbose_name=_('name'))
    amount = models.IntegerField(verbose_name=_('amount'), default=0)
    article = models.CharField(max_length=25, default='NOTARTICLE', blank=True, verbose_name=_('article'))
    full_description = models.TextField(max_length=1000, default='NOTDESCRIPTION', blank=True, verbose_name=_('full_description'))

    class Meta:
        verbose_name = _('product in the store')
        verbose_name_plural = _('products in the store')

    def save(self, *args, **kwargs):
        obj = ProductProfile.objects.get(article=self.name.article)
        obj.amount = F('amount') + self.amount
        obj.save()
        self.article = str(self.name.article) + ',' + str(self.in_shop_id)
        data_1 = self.name.__dict__
        del data_1['_state']
        del data_1['description']
        data_2 = self.in_shop.__dict__
        del data_2['_state']
        del data_2['description']
        del data_2['data_of_birth']
        self.full_description = str(data_1) + str(data_2)
        super(ProductInShop, self).save(*args, **kwargs)
        # full_amount = 0
        # for i in ProductInShop.objects.all():
        #     if i.name_id == self.name_id:
        #         full_amount += i.amount
        # obj = ProductProfile.objects.get(id=self.name_id)
        # obj.amount = full_amount
        # obj.save()

    def __str__(self):
        return self.name.name


class UserGarbage(models.Model):
    """
    Shopping cart for temporary storage of goods added by
    the user before the final order is placed.
    After placing an order, it is cleared from a specific user.
    """
    name = models.CharField(max_length=39, blank=True, verbose_name=_('name'))
    product = models.ForeignKey(ProductInShop, on_delete=models.CASCADE, verbose_name=_('product'))
    shop = models.ForeignKey(ShopProfile, on_delete=models.CASCADE,
                             verbose_name=_('shop'), null=True, default=1)
    amount = models.IntegerField(verbose_name=_('amount'), default=0)
    sum = models.FloatField(verbose_name=_('sum'), default=0)
    full_description = models.TextField(max_length=1000, default='NOTDESCRIPTION', blank=True,
                                        verbose_name=_('full_description'))


class UserBasket(models.Model):
    """
    Shopping cart of goods selected by the user for payment and checkout. If
    there are funds on the user's account,
    they are debited automatically and the goods acquire the "paid" status.
    """
    STATUS_CHOICES = [
        ('y', _('item paid')),
        ('n', _('item not paid'))
    ]
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_('user'))
    product_name = models.CharField(max_length=39, blank=True, verbose_name=_('product_name'))
    product_price = models.FloatField(verbose_name=_('product_price'), default=0)
    amount = models.IntegerField(verbose_name=_('amount'), default=0)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='n', verbose_name=_('status'))
    shop_id = models.IntegerField(verbose_name=_('shop_id'), default=0)
    creation_data = models.DateField(auto_now_add=True, null=True)
    product_photo = models.CharField(max_length=100, blank=True, default='default.jpg',
                                     verbose_name=_('product_photo'))  # 'photo': 'default.jpg'

    class Meta:
        verbose_name = _('product in user basket')  # как будет отображаться в правах
        verbose_name_plural = _('products in user basket')

    def __str__(self):
        return self.product_name
