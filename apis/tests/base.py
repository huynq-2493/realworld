from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import Article, Tag, Comment

User = get_user_model()


class BaseTestCase(TestCase):
    
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'bio': 'Test bio',
            'image': 'https://example.com/image.jpg'
        }
        
        self.user = User.objects.create_user(**self.user_data)
        
        self.other_user_data = {
            'username': 'otheruser',
            'email': 'other@example.com',
            'password': 'otherpass123'
        }
        
        self.other_user = User.objects.create_user(**self.other_user_data)
    
    def create_article(self, author=None, **kwargs):
        if author is None:
            author = self.user
        
        article_data = {
            'title': 'Test Article',
            'description': 'Test description',
            'body': 'Test body content',
            'slug': 'test-article',
            'author': author,
            **kwargs
        }
        
        return Article.objects.create(**article_data)
    
    def create_tag(self, name='test-tag'):
        return Tag.objects.create(name=name)
    
    def create_comment(self, article=None, author=None, **kwargs):
        if article is None:
            article = self.create_article()
        if author is None:
            author = self.user
        
        comment_data = {
            'body': 'Test comment body',
            'article': article,
            'author': author,
            **kwargs
        }
        
        return Comment.objects.create(**comment_data)


class BaseAPITestCase(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'bio': 'Test bio',
            'image': 'https://example.com/image.jpg'
        }
        
        self.user = User.objects.create_user(**self.user_data)
        
        self.other_user_data = {
            'username': 'otheruser',
            'email': 'other@example.com',
            'password': 'otherpass123'
        }
        
        self.other_user = User.objects.create_user(**self.other_user_data)
    
    def authenticate(self, user=None):
        if user is None:
            user = self.user
        
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    
    def logout(self):
        self.client.credentials()
    
    def create_article(self, author=None, **kwargs):
        if author is None:
            author = self.user
        
        article_data = {
            'title': 'Test Article',
            'description': 'Test description',
            'body': 'Test body content',
            'slug': 'test-article',
            'author': author,
            **kwargs
        }
        
        return Article.objects.create(**article_data)
    
    def create_tag(self, name='test-tag'):
        return Tag.objects.create(name=name)
    
    def create_comment(self, article=None, author=None, **kwargs):
        if article is None:
            article = self.create_article()
        if author is None:
            author = self.user
        
        comment_data = {
            'body': 'Test comment body',
            'article': article,
            'author': author,
            **kwargs
        }
        
        return Comment.objects.create(**comment_data)
