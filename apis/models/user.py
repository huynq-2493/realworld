from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    
    # Relationships
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )
    
    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return self.username
    
    def is_following(self, user):
        return self.following.filter(id=user.id).exists()
    
    def follow(self, user):
        if not self.is_following(user) and self != user:
            self.following.add(user)
    
    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)
    
    @property
    def followers_count(self) -> int:
        return self.followers.count()
    
    @property
    def following_count(self) -> int:
        return self.following.count()
