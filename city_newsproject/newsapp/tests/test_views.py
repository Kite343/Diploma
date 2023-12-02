from django.test import TestCase
from ..forms import *
from ..models import *
from django.contrib.auth import get_user_model

class NewsHomeTest(TestCase):
    def setUp(self):
        self.news_list = []
        number_of_nwes = 22
        self.cat =Category.objects.create(name = 'test_news_home',
                                slug = 'test_news_home')
        self.cat.save()
        for i in range(number_of_nwes):
            news = News.objects.create(title = f"test NewsModel {i}",
                            slug = f"test_NewsModel_{i}",
                            content = "test content",
                            is_published = True,
                            cat = self.cat)
            news.save()
            self.news_list.append(news)

    def tearDown(self):
        for news in self.news_list:
            news.delete()
        self.cat.delete()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        error_name: str = f'Ошибка: "home" ожидал шаблон "newsapp/index.html"'
        self.assertTemplateUsed(response, 'newsapp/index.html', error_name)
        

    def test_pagination_is_10(self):
        response = self.client.get(reverse('home'))
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['posts']), 10)

    def test_last_page(self): 
        response = self.client.get(reverse('home') + '?page=3')  
        self.assertEqual(len(response.context['posts']), 2)

    def test_menu_guest_client(self):
        menu = ["О сайте", "Контакты"]
        response = self.client.get(reverse('home'))
        self.assertFalse("Добавить статью" in response.content.decode())
        for m in menu:
            self.assertIn(m, response.content.decode())
            self.assertIn(m, response.content.decode())


class AddPageTest(TestCase):
    def setUp(self):
        self.cat =Category.objects.create(name = 'test_news',
                                slug = 'test_news')
        self.cat.save()

    def tearDown(self):
        self.cat.delete()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/addpage/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('add_page'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('add_page'))
        error_name: str = f'Ошибка: "add_page" ожидал шаблон "newsapp/addpage.html"'
        self.assertTemplateUsed(response, 'newsapp/addpage.html', error_name)

    def test_forms(self):
        user = get_user_model().objects.create_user(
            username='abc', email='abc@gmail.com', password='1234', is_staff = True)
        user.save()
        response = self.client.post('/users/login/', {'username': 'abc', 'password': '1234'})
        
        response = self.client.get(reverse('add_page'))
        self.assertEqual(response.status_code, 200)

        data={"title": "test valid", "slug": "test invalid", "content": "", "cat": self.cat}
        response = self.client.post(reverse('add_page'), data)        
        self.assertFormError(response, 'form', "slug",
                              'Значение должно состоять только из латинских букв, цифр, знаков подчеркивания или дефиса.')
        user.delete()

    