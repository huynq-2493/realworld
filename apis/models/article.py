from django.db import models
from django.conf import settings


class Article(models.Model):
    slug = models.SlugField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Relationships
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='articles'
    )
    tags = models.ManyToManyField('Tag', blank=True, related_name='articles')
    favorited_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='favorited_articles'
    )

    def __str__(self):
        return self.title
    
    @property
    def favorites_count(self):
        return self.favorited_by.count()
    
    def is_favorited_by(self, user):
        if user.is_anonymous:
            return False
        return self.favorited_by.filter(id=user.id).exists()
