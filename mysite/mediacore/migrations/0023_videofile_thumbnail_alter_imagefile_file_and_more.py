# Generated by Django 4.1.5 on 2023-07-02 23:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediacore', '0022_alter_imagefile_file_alter_videofile_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='videofile',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='post_media/2023/07/03'),
        ),
        migrations.AlterField(
            model_name='imagefile',
            name='file',
            field=models.ImageField(upload_to='post_media/2023/07/03', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('jpg', 'png', 'gif', 'webp', 'jpeg'))], verbose_name='файл'),
        ),
        migrations.AlterField(
            model_name='videofile',
            name='file',
            field=models.FileField(upload_to='post_media/2023/07/03', verbose_name='файл'),
        ),
    ]