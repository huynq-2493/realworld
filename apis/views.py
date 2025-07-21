from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models.article import Article
from .models.tag import Tag
from .serializers.article_serializers import ArticleSerializer, ArticleListSerializer
from .serializers.tag_serializers import TagSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'articles': serializer.data,
            'articlesCount': queryset.count()
        })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ArticleSerializer(instance)
        return Response({'article': serializer.data})


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        tag_names = [tag['name'] for tag in serializer.data]
        return Response({'tags': tag_names})
