from rest_framework import serializers
from ..models.article import Article
from ..models.user import User
from ..models.tag import Tag


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'bio', 'image']


class ArticleSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    tagList = serializers.SerializerMethodField()
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)

    class Meta:
        model = Article
        fields = [
            'slug', 'title', 'description', 'body', 'tagList',
            'createdAt', 'updatedAt', 'author'
        ]

    def get_tagList(self, obj):
        return [tag.name for tag in obj.tags.all()]


class ArticleListSerializer(ArticleSerializer):
    class Meta:
        model = Article
        fields = [
            'slug', 'title', 'description', 'tagList',
            'createdAt', 'updatedAt', 'author'
        ]
