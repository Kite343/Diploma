from django.test import TestCase
from ..forms import *

class AddPostFormTest(TestCase):
    def test_field_labels(self):
        form = AddPostForm()
        
