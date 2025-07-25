import django_filters
from django_filters import rest_framework as filters
from .models.article import Article
from .models.user import User
from .models.tag import Tag


class ArticleFilter(filters.FilterSet):
    tag = filters.CharFilter(field_name='tags__name', lookup_expr='iexact')
    author = filters.CharFilter(field_name='author__username', lookup_expr='iexact')
    favorited = filters.CharFilter(method='filter_favorited')
    
    class Meta:
        model = Article
        fields = ['tag', 'author', 'favorited']
    
    def filter_favorited(self, queryset, name, value):
        try:
            user = User.objects.get(username=value)
            return queryset.filter(favorited_by=user)
        except User.DoesNotExist:
            return queryset.none()
