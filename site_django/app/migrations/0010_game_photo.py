# Generated by Django 4.2.1 on 2023-12-18 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_uploadfiles_alter_game_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='photo',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='photos/%Y/%m/%d/', verbose_name='Фото'),
        ),
    ]