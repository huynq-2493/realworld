from typing import Optional, List
from django.db import transaction
from django.utils.text import slugify
from django.core.cache import cache

from ..models.article import Article
from ..models.user import User
from ..models.tag import Tag
from ..models.comment import Comment
from ..constants import TAGS_LIST_CACHE_KEY, CACHE_TIMEOUT_5_MINUTES


class ArticleService:
    @staticmethod
    def create_article(
        author: User, 
        title: str, 
        description: str, 
        body: str, 
        tag_list: Optional[List[str]] = None
    ) -> Article:
        with transaction.atomic():
            # Generate unique slug
            base_slug = slugify(title)
            slug = base_slug
            counter = 1
            
            while Article.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            article = Article.objects.create(
                author=author,
                title=title,
                description=description,
                body=body,
                slug=slug
            )
            
            if tag_list:
                ArticleService._add_tags_to_article(article, tag_list)
            
            return article
    
    @staticmethod
    def update_article(
        article: Article, 
        title: Optional[str] = None,
        description: Optional[str] = None,
        body: Optional[str] = None,
        tag_list: Optional[List[str]] = None
    ) -> Article:
        with transaction.atomic():
            if title and title != article.title:
                article.title = title
                # Regenerate slug if title changed
                base_slug = slugify(title)
                slug = base_slug
                counter = 1
                
                while Article.objects.filter(slug=slug).exclude(pk=article.pk).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                
                article.slug = slug
            
            if description:
                article.description = description
            
            if body:
                article.body = body
            
            article.save()
            
            if tag_list is not None:
                article.tags.clear()
                ArticleService._add_tags_to_article(article, tag_list)
            
            return article
    
    @staticmethod
    def favorite_article(user: User, article: Article) -> Article:
        with transaction.atomic():
            if not article.is_favorited_by(user):
                article.favorited_by.add(user)
            return article
    
    @staticmethod
    def unfavorite_article(user: User, article: Article) -> Article:
        with transaction.atomic():
            if article.is_favorited_by(user):
                article.favorited_by.remove(user)
            return article
    
    @staticmethod
    def add_comment(user: User, article: Article, body: str) -> Comment:
        with transaction.atomic():
            comment = Comment.objects.create(
                author=user,
                article=article,
                body=body
            )
            return comment
    
    @staticmethod
    def delete_comment(user: User, comment: Comment) -> bool:
        if comment.author != user:
            raise PermissionError("You can only delete your own comments")
        
        with transaction.atomic():
            comment.delete()
            return True
    
    @staticmethod
    def get_feed_articles(user: User):
        following_users = user.following.all()
        return Article.objects.filter(
            author__in=following_users
        ).select_related('author').prefetch_related('tags').order_by('-created_at')
    
    @staticmethod
    def _add_tags_to_article(article: Article, tag_names: List[str]) -> None:
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            article.tags.add(tag)
        
        cache.delete(TAGS_LIST_CACHE_KEY)
