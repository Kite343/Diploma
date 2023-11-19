from django.test import TestCase
from ..forms import *
from ..models import *

class AddPostFormTest(TestCase):
    """Тест формы AddPost"""
    def setUp(self):
        self.cat = Category.objects.create(name = 'test_news',
                                slug = 'test_news')
        self.cat.save()

    def tearDown(self):
        self.cat.delete()

    def test_field_labels(self):
        """Тест лейблов полей формы AddPost"""
        form = AddPostForm()

        title_label = form.fields['title'].label
        self.assertEqual(title_label, 'Заголовок')

        title_label = form.fields['slug'].label
        self.assertEqual(title_label, "URL")

        title_label = form.fields['content'].label
        self.assertEqual(title_label, "Текст статьи")

        title_label = form.fields['photo'].label
        self.assertEqual(title_label, "Фото")

        title_label = form.fields['cat'].label
        self.assertEqual(title_label, "Категория")

    def test_field_empty_labels(self):
        """Тест empty_labels полей формы AddPost"""
        form = AddPostForm()

        title_label = form.fields['cat'].empty_label
        self.assertEqual(title_label, "Категория не выбрана")

    def test_is_invalid(self):
        """Тест не валидной формы"""
        form = AddPostForm(data={"title": "test invalid", "slug": "test invalid", "content": "", "cat": self.cat})
        self.assertFalse(form.is_valid())

    def test_form_is_valid(self):
        """Тест валидной формы"""
        form = AddPostForm(data={"title": "test valid", "slug": "test_valid", "content": "", "cat": self.cat})
        self.assertTrue(form.is_valid())

    






