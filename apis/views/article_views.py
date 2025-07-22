from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from ..models.article import Article
from ..models.comment import Comment
from ..models.user import User
from ..serializers.article_serializers import ArticleSerializer, ArticleListSerializer
from ..serializers.comment_serializers import CommentSerializer, CommentCreateSerializer


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

    @action(detail=True, methods=['get', 'post'], url_path='comments')
    def comments(self, request, slug=None):
        article = self.get_object()
        if request.method == 'GET':
            comments = Comment.objects.filter(
                article=article).select_related('author')
            serializer = CommentSerializer(comments, many=True)
            return Response({'comments': serializer.data})

        elif request.method == 'POST':
            comment_data = request.data.get('comment', {})
            serializer = CommentCreateSerializer(data=comment_data)

            if serializer.is_valid():
                author = User.objects.first()
                comment = serializer.save(article=article, author=author)
                response_serializer = CommentSerializer(comment)
                return Response({'comment': response_serializer.data}, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
