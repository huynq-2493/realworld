from typing import Optional
from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken

from ..models.user import User
from ..constants import INVALID_CREDENTIALS, USER_ACCOUNT_DISABLED


class UserService:
    @staticmethod
    def create_user(username: str, email: str, password: str, **extra_fields) -> User:
        with transaction.atomic():
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                **extra_fields
            )
            return user
    
    @staticmethod
    def authenticate_user(email: str, password: str) -> User:
        try:
            user = User.objects.get(email=email)
            authenticated_user = authenticate(username=user.username, password=password)
            
            if not authenticated_user:
                raise ValueError(INVALID_CREDENTIALS)
                
            if not authenticated_user.is_active:
                raise ValueError(USER_ACCOUNT_DISABLED)
                
            return authenticated_user
            
        except User.DoesNotExist:
            raise ValueError(INVALID_CREDENTIALS)
    
    @staticmethod
    def update_user(user: User, **fields) -> User:
        with transaction.atomic():
            password = fields.pop('password', None)
            
            for field, value in fields.items():
                setattr(user, field, value)
            
            if password:
                user.set_password(password)
            
            user.save()
            return user
    
    @staticmethod
    def follow_user(follower: User, followed: User) -> bool:
        if follower == followed:
            raise ValueError("You cannot follow yourself")
        
        with transaction.atomic():
            follower.follow(followed)
            return True
    
    @staticmethod
    def unfollow_user(follower: User, followed: User) -> bool:
        with transaction.atomic():
            follower.unfollow(followed)
            return True
    
    @staticmethod
    def generate_tokens(user: User) -> dict:
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
