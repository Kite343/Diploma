from django.test import TestCase

class TestNews(TestCase):

    # тестирование главной страницы
    def test_index(self):
        """тестирование главной страницы """
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Все категории', response.content.decode())