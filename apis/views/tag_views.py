from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from ..models.tag import Tag
from ..serializers.tag_serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        tag_names = [tag['name'] for tag in serializer.data]
        return Response({'tags': tag_names})
