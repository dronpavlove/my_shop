# Generated by Django 4.0.1 on 2022-01-31 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='category name')),
                ('icon_field', models.ImageField(default='default.jpg', upload_to='category_icon', verbose_name='photo')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='ProductInShop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0, verbose_name='amount')),
            ],
            options={
                'verbose_name': 'product in the store',
                'verbose_name_plural': 'products in the store',
            },
        ),
        migrations.CreateModel(
            name='Promotions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='promotion name')),
                ('description', models.TextField(blank=True, max_length=5000, verbose_name='description')),
                ('status', models.CharField(choices=[('y', 'current'), ('n', 'inactive')], default='y', max_length=1, verbose_name='status')),
            ],
            options={
                'verbose_name': 'promotion',
                'verbose_name_plural': 'promotions',
            },
        ),
        migrations.CreateModel(
            name='ShopProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=39, verbose_name='name')),
                ('description', models.TextField(blank=True, max_length=500, verbose_name='description')),
                ('city', models.CharField(blank=True, max_length=39, verbose_name='city')),
                ('street', models.CharField(blank=True, max_length=50, verbose_name='street')),
                ('house_number', models.IntegerField(default=0, verbose_name='house number')),
                ('data_of_birth', models.DateField(blank=True, null=True, verbose_name='date of formation')),
                ('phone', models.CharField(blank=True, max_length=15, null=True, verbose_name='phone')),
                ('email', models.EmailField(blank=True, max_length=30, null=True, verbose_name='email')),
                ('purchases_count', models.IntegerField(default=0, verbose_name='number of purchases')),
                ('photo', models.ImageField(default='default.jpg', upload_to='shop_photo')),
            ],
            options={
                'verbose_name': 'shop profile',
                'verbose_name_plural': 'shops profile',
            },
        ),
        migrations.CreateModel(
            name='UserGarbage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=39, verbose_name='name')),
                ('amount', models.IntegerField(default=0, verbose_name='amount')),
                ('sum', models.FloatField(default=0, verbose_name='sum')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_shops.productinshop', verbose_name='product')),
                ('shop', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_shops.shopprofile', verbose_name='shop')),
            ],
        ),
        migrations.CreateModel(
            name='UserBasket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(blank=True, max_length=39, verbose_name='product_name')),
                ('product_price', models.FloatField(default=0, verbose_name='product_price')),
                ('amount', models.IntegerField(default=0, verbose_name='amount')),
                ('status', models.CharField(choices=[('y', 'item paid'), ('n', 'item not paid')], default='n', max_length=1, verbose_name='status')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_users.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'product in user basket',
                'verbose_name_plural': 'products in user basket',
            },
        ),
        migrations.CreateModel(
            name='ProductProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.CharField(blank=True, default='NOTARTICLE', max_length=25, verbose_name='article')),
                ('name', models.CharField(blank=True, max_length=39, verbose_name='name')),
                ('description', models.TextField(blank=True, max_length=500, verbose_name='description')),
                ('price', models.FloatField(default=0, verbose_name='price')),
                ('photo', models.ImageField(default='default.jpg', upload_to='product_photo', verbose_name='photo')),
                ('amount', models.IntegerField(default=0, verbose_name='amount')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_shops.category')),
            ],
            options={
                'verbose_name': 'product profile',
                'verbose_name_plural': 'products profile',
            },
        ),
        migrations.AddField(
            model_name='productinshop',
            name='in_shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_shops.shopprofile', verbose_name='name'),
        ),
        migrations.AddField(
            model_name='productinshop',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_shops.productprofile', verbose_name='name'),
        ),
    ]
