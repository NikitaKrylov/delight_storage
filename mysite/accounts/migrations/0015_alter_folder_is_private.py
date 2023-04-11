# Generated by Django 4.1.5 on 2023-04-01 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_folder_is_private'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='is_private',
            field=models.BooleanField(default=True, help_text='другие пользователи смогут видеть содержимое папки', verbose_name='приватная папка'),
        ),
    ]