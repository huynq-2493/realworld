from django.db import models
from django.conf import settings


class Comment(models.Model):
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Relationships
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    article = models.ForeignKey(
        'Article',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Comment by {self.author.username} on {self.article.title}"
