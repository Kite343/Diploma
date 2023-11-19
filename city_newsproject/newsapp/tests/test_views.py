from django.test import TestCase
from ..forms import *
from ..models import *

# class TestNewsUrls(TestCase):
#     # тестирование главной страницы
#     def test_index(self):
#         """тестирование главной страницы """
#         response = self.client.get('')
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('Все категории', response.content.decode())

class NewsHomeTest(TestCase):
    def setUp(self):
        number_of_nwes = 22
        self.cat =Category.objects.create(name = 'test_news_home',
                                slug = 'test_news_home')
        # self.cat.save()
        for i in range(number_of_nwes):
            news = News.objects.create(title = f"test NewsModel {i}",
                            slug = f"test_NewsModel_{i}",
                            content = "test content",
                            is_published = True,
                            cat = self.cat)
            # news.save()

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
        # self.assertTrue( len(response.context['posts']) == 10)
        self.assertEqual(len(response.context['posts']), 10)

    def test_last_page(self): 
        response = self.client.get(reverse('home') + '?page=3') 
        # self.assertTrue( len(response.context['posts']) == 2)  
        self.assertEqual(len(response.context['posts']), 2)




    