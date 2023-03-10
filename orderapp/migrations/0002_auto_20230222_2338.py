# Generated by Django 3.2.18 on 2023-02-22 20:38

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('paymentapp', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('orderapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(db_index=True, verbose_name='Активен')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(db_index=True, verbose_name='Активен')),
            ],
            options={
                'verbose_name': 'Менеджер',
                'verbose_name_plural': 'Менеджеры',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Создана')),
                ('estimated_at', models.DateTimeField(blank=True, null=True, verbose_name='Истекает')),
                ('finished_at', models.DateTimeField(blank=True, null=True, verbose_name='Закрыта')),
                ('status', models.CharField(choices=[('NEW', 'Новый'), ('WOR', 'В работе'), ('FIN', 'Завершен'), ('OVE', 'Просрочен')], db_index=True, max_length=3, verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Заявки',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('tg_chat_id', models.CharField(max_length=64, null=True, unique=True, verbose_name='ID чата Телеграм')),
                ('tg_username', models.CharField(blank=True, max_length=64, null=True, verbose_name='Имя пользователя в Телеграм')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(verbose_name='Дата оформления')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribtions', to='orderapp.client', verbose_name='Клиент')),
                ('tariff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subscribtions', to='paymentapp.tariff', verbose_name='Тариф')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Создано')),
                ('closed_at', models.DateTimeField(blank=True, null=True, verbose_name='Закрыто')),
                ('status', models.CharField(choices=[('NEW', 'Новое'), ('WOR', 'В работе'), ('CLO', 'Закрыто')], db_index=True, max_length=3, verbose_name='Статус')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='orderapp.manager', verbose_name='Ответственный менеджер')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tickets', to='orderapp.order', verbose_name='По заявке')),
            ],
            options={
                'verbose_name': 'Обращение',
                'verbose_name_plural': 'Обращения',
            },
        ),
        migrations.CreateModel(
            name='Сontractor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(db_index=True, verbose_name='Активен')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contractors', to='orderapp.person', verbose_name='Учетная запись Телеграм')),
            ],
            options={
                'verbose_name': 'Подрядчик',
                'verbose_name_plural': 'Подрядчики',
            },
        ),
        migrations.DeleteModel(
            name='Tg_user',
        ),
        migrations.AddField(
            model_name='order',
            name='contractor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='orderapp.сontractor', verbose_name='Исполнитель'),
        ),
        migrations.AddField(
            model_name='order',
            name='subscription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='orderapp.subscription', verbose_name='Подписка'),
        ),
        migrations.AddField(
            model_name='manager',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='managers', to='orderapp.person', verbose_name='Учетная запись Телеграм'),
        ),
        migrations.AddField(
            model_name='client',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clients', to='orderapp.person', verbose_name='Учетная запись Телеграм'),
        ),
    ]
