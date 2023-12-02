from django.test import TestCase
from ..models import *

class NewsModelTest(TestCase):
    """Тест Модели NewsModel"""

    def setUp(self):
        self.cat =Category.objects.create(name = 'test_news',
                                slug = 'test_news')
        self.cat.save()
        self.news = News.objects.create(title = "test NewsModel",
                            slug = "test_NewsModel",
                            content = "test content",
                            is_published = True,
                            cat = self.cat)
        self.news.save()
        
    def tearDown(self):
        self.news.delete()
        self.cat.delete()
        
        
    def test_title_label(self):
        """test label for title"""
        field_label = self.news._meta.get_field('title').verbose_name
        self.assertEquals(field_label, "Заголовок")

    def test_title_max_length(self):
        """test max_length for title"""
        max_length = self.news._meta.get_field('title').max_length
        self.assertEquals(max_length, 255)

    def test_slug_label(self):
        """test label for slug"""
        field_label = self.news._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, "URL")

    def test_slug_max_length(self):
        """test max_length for slug"""
        max_length = self.news._meta.get_field('slug').max_length
        self.assertEquals(max_length, 255)

    def test_slug_unique(self):
        """test unique for slug"""
        slug_field = self.news._meta.get_field('slug')
        real_unique = getattr(slug_field, 'unique')
        self.assertEqual(real_unique, True)

    def test_content_label(self):
        """test label for content"""
        field_label = self.news._meta.get_field('content').verbose_name
        self.assertEquals(field_label, "Текст статьи")

    def test_photo_label(self):
        """test label for photo"""
        field_label = self.news._meta.get_field('photo').verbose_name
        self.assertEquals(field_label, "Фото")

    def test_time_create_label(self):
        """test label for time_create"""
        field_label = self.news._meta.get_field('time_create').verbose_name
        self.assertEquals(field_label, "Время создания")

    def test_time_create_auto_now_add(self):
        """test auto_now_add for time_create"""
        time_create_field = self.news._meta.get_field('time_create')
        auto = getattr(time_create_field, 'auto_now_add')
        self.assertEqual(auto, True)

    def test_time_update_label(self):
        """test label for time_update"""
        field_label = self.news._meta.get_field('time_update').verbose_name
        self.assertEquals(field_label, "Время изменения")

    def test_time_update_auto_now(self):
        """test auto_now for time_update"""
        time_update_field = self.news._meta.get_field('time_update')
        auto = getattr(time_update_field, 'auto_now')
        self.assertEqual(auto, True)

    def test_cat_label(self):
        """test label for cat"""
        field_label = self.news._meta.get_field('cat').verbose_name
        self.assertEquals(field_label, "Категория")

    def test_cat_on_delete(self):
        """test on_delete for cat"""
        cat_field = self.news._meta.get_field('cat')
        on_delete_param = cat_field.remote_field.on_delete
        self.assertEqual(on_delete_param, models.PROTECT)

    def test_get_absolute_url(self):
        """test get_absolute_url"""
        self.assertEquals(self.news.get_absolute_url(), f'/post/{self.news.slug}/')

    def test_create_news(self):
        """test create news"""
        self.assertEqual(self.news.title, 'test NewsModel')
        self.assertEqual(self.news.cat, self.cat)

    def test_news_str(self):   
        """test str for news"""     
        self.assertEqual(str(self.news), 'test NewsModel')