# Generated by Django 4.1.5 on 2023-02-22 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_rename_recipient_postcomplaint_sender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=255, unique=True, verbose_name='почта'),
        ),
    ]
