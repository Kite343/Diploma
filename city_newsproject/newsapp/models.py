from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

class News(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото", blank=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    # is_published = models.BooleanField(default=True, verbose_name="Публикация")
    is_published = models.BooleanField(default=False, verbose_name="Публикация")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name="Категория")

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})
    
    class Meta:
        verbose_name = 'Новости'
        verbose_name_plural = 'Новости'
        # -time_create обратная, time_create прямая
        ordering = ['-time_create', 'title']


class Category(models.Model):
    # name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
 
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='user_comments', null=True, default=None)
    comment = models.TextField(blank=True, verbose_name="Текст комментария")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-time_create']

    def __str__(self):
        return f"{self.news.title}: {self.author.get_username}: {self.time_create}"
    
class Contact(models.Model):
    type_contact = models.CharField(max_length=100, db_index=True, verbose_name="Тип контакта")
    contact = models.CharField(max_length=100, db_index=True, verbose_name="Контакт")

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        ordering = ['type_contact']

class About(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок", blank=True)
    content = models.TextField(verbose_name="Текст", blank=True)
    photo_1 = models.ImageField(upload_to="about/%Y/%m/%d/", verbose_name="Фото 1", blank=True)
    photo_2 = models.ImageField(upload_to="about/%Y/%m/%d/", verbose_name="Фото 2", blank=True)
    photo_3 = models.ImageField(upload_to="about/%Y/%m/%d/", verbose_name="Фото 3", blank=True)
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    position = models.IntegerField(unique=True)

    class Meta:
        verbose_name = 'контент о сайте'
        verbose_name_plural = 'контент о сайте'
        ordering = ['position']