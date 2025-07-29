from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from ..models.user import User
from ..serializers.user_serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer, 
    UserSerializer,
    UserUpdateSerializer,
    ProfileSerializer
)
from ..throttles import LoginRateThrottle, RegisterRateThrottle


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [RegisterRateThrottle]
    
    def post(self, request):
        user_data = request.data.get('user', {})
        serializer = UserRegistrationSerializer(data=user_data)
        
        if serializer.is_valid():
            user = serializer.save()
            user_serializer = UserSerializer(user)
            return Response({'user': user_serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [LoginRateThrottle]
    
    def post(self, request):
        user_data = request.data.get('user', {})
        serializer = UserLoginSerializer(data=user_data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            user_serializer = UserSerializer(user)
            return Response({'user': user_serializer.data}, status=status.HTTP_200_OK)
        
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data})
    
    def put(self, request):
        user_data = request.data.get('user', {})
        serializer = UserUpdateSerializer(request.user, data=user_data, partial=True)
        
        if serializer.is_valid():
            user = serializer.save()
            user_serializer = UserSerializer(user)
            return Response({'user': user_serializer.data})
        
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'username'
    permission_classes = [AllowAny]
    http_method_names = ['get']

    def get_permissions(self):
        if self.action in ['follow']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        return Response({'profile': serializer.data})
    
    @action(detail=True, methods=['post', 'delete'], url_path='follow', permission_classes=[IsAuthenticated])
    def follow(self, request, username=None):
        profile = self.get_object()
        user = request.user
        
        if user == profile:
            return Response(
                {'error': 'You cannot follow yourself'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if request.method == 'POST':
            user.follow(profile)
            serializer = ProfileSerializer(profile, context={'request': request})
            return Response({'profile': serializer.data})
            
        elif request.method == 'DELETE':
            user.unfollow(profile)
            serializer = ProfileSerializer(profile, context={'request': request})
            return Response({'profile': serializer.data})
