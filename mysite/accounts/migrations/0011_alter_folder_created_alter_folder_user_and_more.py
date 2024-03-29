# Generated by Django 4.1.5 on 2023-03-03 22:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_alter_post_description'),
        ('accounts', '0010_folder_folderpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='дата создания'),
        ),
        migrations.AlterField(
            model_name='folder',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='folders', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AlterField(
            model_name='folderpost',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='дата добавления'),
        ),
        migrations.AlterField(
            model_name='folderpost',
            name='folder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='accounts.folder', verbose_name='папка'),
        ),
        migrations.AlterField(
            model_name='folderpost',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post', verbose_name='пост'),
        ),
    ]
