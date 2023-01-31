# Generated by Django 4.1 on 2023-01-26 22:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_merge_20230113_0117'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostComplaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('CN', 'На рассмотрении'), ('AC', 'Принята'), ('RJ', 'Отклонена')], default='CN', max_length=20, verbose_name='статус')),
                ('type', models.CharField(choices=[('BT', 'Несоответствие тегам'), ('BM', 'Неподходящие/плохие медиа'), ('PL', 'Плагиат'), ('AN', 'Еще')], default='BT', max_length=40, verbose_name='тип жалобы')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('description', models.TextField(blank=True, max_length=200, null=True, verbose_name='описание')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complaints', to=settings.AUTH_USER_MODEL, verbose_name='отправитель')),
            ],
            options={
                'verbose_name': 'Жалоба',
                'verbose_name_plural': 'Жалобы',
            },
        ),
        migrations.DeleteModel(
            name='Complaint',
        ),
    ]
