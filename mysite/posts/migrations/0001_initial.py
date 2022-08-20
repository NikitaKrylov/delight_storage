# Generated by Django 4.1 on 2022-08-20 03:39

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PostTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=30, verbose_name='название тега')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='VideoPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publication_date', models.DateField(auto_now_add=True, verbose_name='дата публикации')),
                ('only_for_adult', models.BooleanField(default=False, verbose_name='18+ контент')),
                ('for_autenticated_users', models.BooleanField(default=False, verbose_name='для авторизированных пользователей')),
                ('for_premium_users', models.BooleanField(default=False, verbose_name='для премиум пользователей')),
                ('disable_comments', models.BooleanField(default=False, verbose_name='запретить коментарии')),
                ('post_author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='автор поста')),
                ('tags', models.ManyToManyField(to='posts.posttag', verbose_name='теги')),
            ],
            options={
                'verbose_name': 'Видео пост',
                'verbose_name_plural': 'Видео посты',
            },
        ),
        migrations.CreateModel(
            name='TextPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publication_date', models.DateField(auto_now_add=True, verbose_name='дата публикации')),
                ('only_for_adult', models.BooleanField(default=False, verbose_name='18+ контент')),
                ('for_autenticated_users', models.BooleanField(default=False, verbose_name='для авторизированных пользователей')),
                ('for_premium_users', models.BooleanField(default=False, verbose_name='для премиум пользователей')),
                ('disable_comments', models.BooleanField(default=False, verbose_name='запретить коментарии')),
                ('title', models.CharField(max_length=150, verbose_name='заголовок')),
                ('body', models.TextField(blank=True, null=True, verbose_name='текст')),
                ('post_author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='автор поста')),
                ('tags', models.ManyToManyField(to='posts.posttag', verbose_name='теги')),
            ],
            options={
                'verbose_name': 'Текстовые пост',
                'verbose_name_plural': 'Текстовые посты',
            },
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveBigIntegerField(validators=[django.core.validators.MaxValueValidator(5)], verbose_name='оценка')),
                ('object_id', models.PositiveIntegerField(verbose_name='id объекта')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='автор оценки')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype', verbose_name='тип оцениваемого объекта')),
            ],
            options={
                'verbose_name': 'Оценка',
                'verbose_name_plural': 'Оценки',
            },
        ),
        migrations.CreateModel(
            name='ImagePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publication_date', models.DateField(auto_now_add=True, verbose_name='дата публикации')),
                ('only_for_adult', models.BooleanField(default=False, verbose_name='18+ контент')),
                ('for_autenticated_users', models.BooleanField(default=False, verbose_name='для авторизированных пользователей')),
                ('for_premium_users', models.BooleanField(default=False, verbose_name='для премиум пользователей')),
                ('disable_comments', models.BooleanField(default=False, verbose_name='запретить коментарии')),
                ('post_author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='автор поста')),
                ('tags', models.ManyToManyField(to='posts.posttag', verbose_name='теги')),
            ],
            options={
                'verbose_name': 'Фото пост',
                'verbose_name_plural': 'Фото посты',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(verbose_name='id объекта')),
                ('text', models.TextField(verbose_name='текст')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='автор')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype', verbose_name='тип коментируемого объекта')),
            ],
            options={
                'verbose_name': 'Коментарий',
                'verbose_name_plural': 'Коментарии',
            },
        ),
    ]
