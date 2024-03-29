# Generated by Django 4.1 on 2023-01-26 22:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_alter_post_description'),
        ('accounts', '0006_postcomplaint_delete_complaint'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postcomplaint',
            options={'verbose_name': 'Жалоба на пост', 'verbose_name_plural': 'Жалобы на посты'},
        ),
        migrations.AddField(
            model_name='postcomplaint',
            name='post',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='complaints', to='posts.post'),
            preserve_default=False,
        ),
    ]
