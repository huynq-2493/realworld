
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .base import BaseTestCase

User = get_user_model()


class UserModelTestCase(BaseTestCase):
    
    def test_user_creation(self):
        self.assertTrue(isinstance(self.user, User))
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.bio, 'Test bio')
        self.assertTrue(self.user.check_password('testpass123'))
    
    def test_user_str_representation(self):
        self.assertEqual(str(self.user), 'testuser')
    
    def test_user_follow_functionality(self):
        # Initially not following
        self.assertFalse(self.user.is_following(self.other_user))
        
        # Follow user
        self.user.follow(self.other_user)
        self.assertTrue(self.user.is_following(self.other_user))
        
        # Following count
        self.assertEqual(self.user.following.count(), 1)
        self.assertEqual(self.other_user.followers.count(), 1)
        
        # Unfollow user
        self.user.unfollow(self.other_user)
        self.assertFalse(self.user.is_following(self.other_user))
        self.assertEqual(self.user.following.count(), 0)
    
    def test_user_cannot_follow_themselves(self):
        initial_count = self.user.following.count()
        self.user.follow(self.user)
        self.assertEqual(self.user.following.count(), initial_count)
    
    def test_user_cannot_follow_twice(self):
        self.user.follow(self.other_user)
        self.user.follow(self.other_user)  # Try to follow again
        
        self.assertEqual(self.user.following.count(), 1)
        self.assertEqual(self.other_user.followers.count(), 1)
    
    def test_unfollow_user_not_following(self):
        initial_count = self.user.following.count()
        self.user.unfollow(self.other_user)
        self.assertEqual(self.user.following.count(), initial_count)
