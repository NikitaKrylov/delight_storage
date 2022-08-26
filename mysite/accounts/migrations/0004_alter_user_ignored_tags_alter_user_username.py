# Generated by Django 4.1 on 2022-08-23 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_alter_like_options_posttag_slug_alter_posttag_name'),
        ('accounts', '0003_clientip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='ignored_tags',
            field=models.ManyToManyField(blank=True, to='posts.posttag', verbose_name='игнорируемые теги'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=50, unique=True, verbose_name='имя пользователя'),
        ),
    ]