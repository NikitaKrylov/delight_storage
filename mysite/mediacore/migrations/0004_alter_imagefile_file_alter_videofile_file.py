# Generated by Django 4.1 on 2023-01-12 22:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediacore', '0003_alter_imagefile_file_alter_videofile_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagefile',
            name='file',
            field=models.ImageField(upload_to='post_media/2023/01/13', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('jpg', 'png', 'gif', 'webp', 'jpeg'))], verbose_name='файл'),
        ),
        migrations.AlterField(
            model_name='videofile',
            name='file',
            field=models.FileField(upload_to='post_media/2023/01/13', verbose_name='файл'),
        ),
    ]
