from django.contrib.auth.models import User
from django.test import TestCase
from .serializers import BookSerializer
from .models import Book


class SerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='password')
        self.book = Book.objects.create(title='Alice in Wonderland', author='Linda Woolverton', description='Description', price=500, owner=self.user)

    def test_data(self):
        data = BookSerializer(self.book).data
        expected_data = {
            'id': self.book.id,
            'title': 'Alice in Wonderland',
            'author': 'Linda Woolverton',
            'description': 'Description',
            'price': '500.00',
            'owner': self.user.id,
            'cover': None

        }
        self.assertEqual(expected_data, data)
