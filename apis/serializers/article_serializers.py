from rest_framework import serializers
from ..models.article import Article
from ..models.user import User
from ..models.tag import Tag
from .user_serializers import ProfileSerializer


class ArticleSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    tagList = serializers.SerializerMethodField()
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)
    favorited = serializers.SerializerMethodField()
    favoritesCount = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'slug', 'title', 'description', 'body', 'tagList',
            'createdAt', 'updatedAt', 'favorited', 'favoritesCount', 'author'
        ]

    def get_tagList(self, obj):
        return [tag.name for tag in obj.tags.all()]
    
    def get_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.is_favorited_by(request.user)
        return False
    
    def get_favoritesCount(self, obj):
        return obj.favorites_count
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'context' in kwargs:
            self.fields['author'].context = kwargs['context']


class ArticleListSerializer(ArticleSerializer):
    class Meta:
        model = Article
        fields = [
            'slug', 'title', 'description', 'tagList',
            'createdAt', 'updatedAt', 'favorited', 'favoritesCount', 'author'
        ]
