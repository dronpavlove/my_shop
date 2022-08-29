from django.test import TestCase, Client
from app_shops.models import *
from django.urls import reverse
from app_users.models import Profile
from django.contrib.auth.models import User


class UsersTest(TestCase):

    urls_list = ['start_shops', 'shops_list', 'basket', 'check',
                 'update_product_list', 'start_users', 'login',
                 'registration', 'purchase_history', 'another_registration/edit']

    def setUp(self):
        #  определяем данные для проверки
        test_user1 = User.objects.create(username='TestUser', password='123@qweasdzxc',
                                         first_name='Andrey', email='test@mail.ru')
        test_user1.save()
        test_user_profile1 = Profile.objects.create(user=test_user1, city='Moscow',
                                                    data_of_birth='1995-05-12', phone=88002000800,
                                                    street='Ageeva', postcode='346282', house_number='64',
                                                    apartment_number='1', )
        test_user_profile1.save()
        test_user2 = User.objects.create(username='TestUserNotProfile', password='123@qweasdzxc',
                                         first_name='TestNotProfile', email='testnotprofile@mail.ru')
        test_user2.save()
        test_shop = ShopProfile.objects.create(name='TestShopProfile', description='TestDescription',
                                               city='TestCity', email='testshop@mail.ru',
                                               street='TestStreet', house_number='1', data_of_birth='1995-05-12',
                                               phone='88001000878')
        test_shop.save()
        test_category = Category.objects.create(name='TestCategory')
        test_category.save()
        self.test_product = ProductProfile.objects.create(name='TestProductProfile',
                                                          category=test_category,
                                                          description='TestDescription', price=10000.99)
        self.test_product_in_shop = ProductInShop.objects.create(name=self.test_product,
                                                                 in_shop=test_shop)
        self.user_garbage_1 = UserGarbage.objects.create(name='TestUser', product=self.test_product_in_shop,
                                                         shop=test_shop,)
        self.user_garbage_2 = UserGarbage.objects.create(name='TestUserNotProfile', product=self.test_product_in_shop,
                                                         shop=test_shop, )

    def test_auth_user_yes_profile(self):
        """
        Прверка доступных ссылок и страниц для юзера с профилем
        :return:
        """
        self.client.force_login(User.objects.get_or_create(username='TestUser')[0])
        resp = self.client.get(reverse('start_page'))
        self.assertContains(resp, 'Welcome to the site')
        self.assertContains(resp, 'User rights information')
        self.assertNotContains(resp, 'You are not authorized on our website')
        self.assertNotContains(resp, 'Simple registration')
        self.assertNotContains(resp, 'Detailed registration')
        self.assertNotContains(resp, 'Login')
        for i in self.urls_list:
            self.error_print(i, 'Для юзера с профилем ')
        self.error_print('shops_detail', 'Для юзера с профилем ', pk=1)
        self.error_print('category_detail', 'Для юзера с профилем ', pk=1)
        self.error_print('product_list', 'Для юзера с профилем ', pk=1, pk1=1)
        self.error_print('product_detail', 'Для юзера с профилем ', pk=1, pk1=1, pk2=1)

    def test_auth_user_no_profile(self):
        """
        Прверка доступных ссылок и страниц для юзера без профиля
        :return:
        """
        self.client.force_login(User.objects.get_or_create(username='TestUserNotProfile')[0])
        resp = self.client.get(reverse('start_page'))
        self.assertContains(resp, 'Welcome to the site')
        self.assertContains(resp, 'User rights information')
        self.assertNotContains(resp, 'You are not authorized on our website')
        self.assertNotContains(resp, 'Simple registration')
        self.assertNotContains(resp, 'Detailed registration')
        self.assertNotContains(resp, 'Login')
        for i in self.urls_list:
            self.error_print(i, 'Для юзера без профиля ')
        self.error_print('shops_detail', 'Для юзера без профиля ', pk=1)
        self.error_print('category_detail', 'Для юзера без профиля ', pk=1)
        self.error_print('product_list', 'Для юзера без профиля ', pk=1, pk1=1)
        self.error_print('product_detail', 'Для юзера без профиля ', pk=1, pk1=1, pk2=1)

    def test_all_users(self):
        """
        Прверка доступных ссылок и страниц для юзера без профиля
        :return:
        """
        resp = self.client.get(reverse('start_page'))
        self.assertNotContains(resp, 'Welcome to the site')
        self.assertContains(resp, 'User rights information')
        self.assertContains(resp, 'You are not authorized on our website')
        self.assertContains(resp, 'Simple registration')
        self.assertContains(resp, 'Detailed registration')
        self.assertContains(resp, 'Login')
        for i in self.urls_list:
            self.error_print(i, 'Для неавторизированного ')
        self.error_print('shops_detail', 'Для неавторизированных ', pk=1)
        self.error_print('category_detail', 'Для неавторизированных ', pk=1)
        self.error_print('product_list', 'Для неавторизированных ', pk=1, pk1=1)
        self.error_print('product_detail', 'Для неавторизированных ', pk=1, pk1=1, pk2=1)

    def error_print(self, url, text, **pk):
        try:
            self.assertEqual(self.client.get(reverse(url, kwargs=pk)).status_code, 200)
        except:
            print(text, '/', url, '/', 'недоступно')
            print('-' * 62)
