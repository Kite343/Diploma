# Generated by Django 4.2.5 on 2023-11-14 10:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('newsapp', '0003_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_contact', models.CharField(db_index=True, max_length=100, verbose_name='Тип контакта')),
                ('contact', models.CharField(db_index=True, max_length=100, verbose_name='Контакт')),
            ],
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-time_create'], 'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='news',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='newsapp.news'),
        ),
        migrations.AlterField(
            model_name='news',
            name='is_published',
            field=models.BooleanField(default=False, verbose_name='Публикация'),
        ),
    ]