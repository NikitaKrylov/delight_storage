# Generated by Django 4.1.5 on 2023-03-27 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_folder_description_folder_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='is_private',
            field=models.BooleanField(default=True, help_text='если True, то другие пользователи смогут просмматривать содержимое папки', verbose_name='приватная папка'),
        ),
    ]