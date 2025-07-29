from rest_framework import serializers
from ..models.comment import Comment
from .user_serializers import ProfileSerializer


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['body']

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'body', 'createdAt', 'updatedAt', 'author']
        read_only_fields = ['id', 'createdAt', 'updatedAt', 'author']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'context' in kwargs:
            self.fields['author'].context = kwargs['context']
