from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    
    objects = UserManager()

    def __str__(self):
        return self.username
