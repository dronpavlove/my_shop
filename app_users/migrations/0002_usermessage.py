# Generated by Django 4.0.1 on 2022-02-05 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, verbose_name='name')),
                ('email', models.EmailField(blank=True, max_length=30, null=True, verbose_name='email')),
                ('message', models.TextField(blank=True, max_length=5000, verbose_name='message')),
                ('status', models.CharField(choices=[('y', 'answered'), ('n', 'unanswered')], default='n', max_length=1, verbose_name='status')),
            ],
            options={
                'verbose_name': 'user message',
                'verbose_name_plural': 'users message',
            },
        ),
    ]
