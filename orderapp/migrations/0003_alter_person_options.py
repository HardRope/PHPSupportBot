# Generated by Django 3.2.18 on 2023-02-22 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orderapp', '0002_auto_20230222_2338'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]
