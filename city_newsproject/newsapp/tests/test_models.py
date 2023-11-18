from django.test import TestCase
from ..models import *

class NewsModelTest(TestCase):
    """Тест Модели NewsModel"""

    def setUp(self):
        # Category.objects.create(name = 'test_news',
        #                         slug = 'test_news')
        # cat = Category.objects.filter(slug='test_news').first()
        self.cat =Category.objects.create(name = 'test_news',
                                slug = 'test_news')
        self.news = News.objects.create(title = "test NewsModel",
                            slug = "test_NewsModel",
                            content = "test content",
                            is_published = True,
                            cat = self.cat)
        
    def test_title_label(self):
        # news = News.objects.filter(slug='test_NewsModel').first()
        # news = News.objects.get(slug='test_NewsModel')
        field_label = self.news._meta.get_field('title').verbose_name
        self.assertEquals(field_label, "Заголовок")

    def test_title_max_length(self):
        # news = News.objects.get(slug='test_NewsModel')
        max_length = self.news._meta.get_field('title').max_length
        self.assertEquals(max_length, 255)

    def test_slug_label(self):
        # news = News.objects.filter(slug='test_NewsModel').first()
        # news = News.objects.get(slug='test_NewsModel')
        field_label = self.news._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, "URL")

    def test_slug_max_length(self):
        # news = News.objects.get(slug='test_NewsModel')
        max_length = self.news._meta.get_field('slug').max_length
        self.assertEquals(max_length, 255)

    def test_slug_unique(self):
        slug_field = self.news._meta.get_field('slug')
        real_unique = getattr(slug_field, 'unique')
        self.assertEqual(real_unique, True)

    def test_content_label(self):
        field_label = self.news._meta.get_field('content').verbose_name
        self.assertEquals(field_label, "Текст статьи")

    def test_photo_label(self):
        field_label = self.news._meta.get_field('photo').verbose_name
        self.assertEquals(field_label, "Фото")

    def test_time_create_label(self):
        field_label = self.news._meta.get_field('time_create').verbose_name
        self.assertEquals(field_label, "Время создания")

    def test_time_create_auto_now_add(self):
        time_create_field = self.news._meta.get_field('time_create')
        auto = getattr(time_create_field, 'auto_now_add')
        self.assertEqual(auto, True)

    def test_time_update_label(self):
        field_label = self.news._meta.get_field('time_update').verbose_name
        self.assertEquals(field_label, "Время изменения")

    def test_time_update_auto_now(self):
        time_update_field = self.news._meta.get_field('time_update')
        auto = getattr(time_update_field, 'auto_now')
        self.assertEqual(auto, True)

    def test_cat_label(self):
        field_label = self.news._meta.get_field('cat').verbose_name
        self.assertEquals(field_label, "Категория")

    def test_cat_on_delete(self):
        cat_field = self.news._meta.get_field('cat')
        on_delete_param = cat_field.remote_field.on_delete
        self.assertEqual(on_delete_param, models.PROTECT)

    def test_get_absolute_url(self):
        self.assertEquals(self.news.get_absolute_url(), f'/post/{self.news.slug}/')

    def test_create_news(self):
        self.assertEqual(self.news.title, 'test NewsModel')
        self.assertEqual(self.news.cat, self.cat)

    def test_news_str(self):
        
        self.assertEqual(str(self.news), 'test NewsModel')