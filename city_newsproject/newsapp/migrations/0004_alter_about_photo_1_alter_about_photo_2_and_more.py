# Generated by Django 4.2.5 on 2023-11-18 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsapp', '0003_about'),
    ]

    operations = [
        migrations.AlterField(
            model_name='about',
            name='photo_1',
            field=models.ImageField(blank=True, upload_to='about/%Y/%m/%d/', verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='about',
            name='photo_2',
            field=models.ImageField(blank=True, upload_to='about/%Y/%m/%d/', verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='about',
            name='photo_3',
            field=models.ImageField(blank=True, upload_to='about/%Y/%m/%d/', verbose_name='Фото'),
        ),
    ]
