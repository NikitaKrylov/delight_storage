# Generated by Django 4.1.5 on 2023-04-30 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_remove_user_role_user_groups_user_is_superuser_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='название')),
                ('image', models.ImageField(upload_to='', verbose_name='иконка')),
                ('color', models.CharField(help_text='цвет указывается в hex формате', max_length=7, verbose_name='цвет')),
                ('description', models.CharField(max_length=255, verbose_name='описание')),
            ],
            options={
                'verbose_name': 'роль',
                'verbose_name_plural': 'роли',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.role', verbose_name='роль'),
        ),
    ]
