from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.cache import cache

from ..models.tag import Tag
from ..serializers.tag_serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        cache_key = "tags_list"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        tag_names = [tag['name'] for tag in serializer.data]
        response_data = {'tags': tag_names}
        cache.set(cache_key, response_data, 300)  # Cache for 5 minutes
        return Response(response_data)
