from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from ..models.article import Article
from ..models.comment import Comment
from ..models.user import User
from ..serializers.article_serializers import ArticleSerializer, ArticleListSerializer
from ..serializers.comment_serializers import CommentSerializer, CommentCreateSerializer
from ..permissions import IsAuthorOrReadOnly
from ..filters import ArticleFilter
from ..pagination import ArticleLimitOffsetPagination
from ..throttles import ArticleCreateThrottle


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().select_related(
        'author').prefetch_related('tags')
    serializer_class = ArticleListSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ArticleFilter
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    search_fields = ['title', 'description', 'body']
    pagination_class = ArticleLimitOffsetPagination
    throttle_classes = [ArticleCreateThrottle]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
        elif self.action in ['feed', 'favorite', 'unfavorite']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ArticleSerializer
        return ArticleListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
            queryset, many=True, context={'request': request})
        return Response({
            'articles': serializer.data,
            'articlesCount': queryset.count()
        })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ArticleSerializer(instance, context={'request': request})
        return Response({'article': serializer.data})

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def feed(self, request):
        following_users = request.user.following.all()
        queryset = Article.objects.filter(author__in=following_users).select_related(
            'author').prefetch_related('tags').order_by('-created_at')
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response({
            'articles': serializer.data,
            'articlesCount': queryset.count()
        })

    @action(detail=True, methods=['post', 'delete'], url_path='favorite', permission_classes=[IsAuthenticated])
    def favorite(self, request, slug=None):
        article = self.get_object()
        user = request.user

        if request.method == 'POST':
            if not article.is_favorited_by(user):
                article.favorited_by.add(user)

            serializer = ArticleSerializer(
                article, context={'request': request})
            return Response({'article': serializer.data})
        elif request.method == 'DELETE':
            if article.is_favorited_by(user):
                article.favorited_by.remove(user)

            serializer = ArticleSerializer(
                article, context={'request': request})
            return Response({'article': serializer.data})

    @action(detail=True, methods=['get', 'post'], url_path='comments')
    def comments(self, request, slug=None):
        article = self.get_object()
        if request.method == 'GET':
            comments = Comment.objects.filter(
                article=article).select_related('author')
            serializer = CommentSerializer(comments, many=True, context={'request': request})
            return Response({'comments': serializer.data})

        elif request.method == 'POST':
            if not request.user.is_authenticated:
                return Response(
                    {'error': 'Authentication required'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            comment_data = request.data.get('comment', {})
            serializer = CommentCreateSerializer(data=comment_data)

            if serializer.is_valid():
                comment = serializer.save(article=article, author=request.user)
                response_serializer = CommentSerializer(comment, context={'request': request})
                return Response({'comment': response_serializer.data}, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'], url_path='comments/(?P<comment_id>[^/.]+)', permission_classes=[IsAuthenticated])
    def delete_comment(self, request, slug=None, comment_id=None):
        article = self.get_object()
        try:
            comment = Comment.objects.get(id=comment_id, article=article)
        except Comment.DoesNotExist:
            return Response(
                {'error': 'Comment not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        if comment.author != request.user:
            return Response(
                {'error': 'You can only delete your own comments'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
