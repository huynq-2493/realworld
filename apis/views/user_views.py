from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.user import User
from ..serializers.user_serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer, 
    UserSerializer,
    UserUpdateSerializer,
    ProfileSerializer
)
from ..services.user_service import UserService
from ..throttles import LoginRateThrottle, RegisterRateThrottle
from ..constants import CANNOT_FOLLOW_YOURSELF
from ..utils.responses import ResponseUtils



class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [RegisterRateThrottle]
    
    def post(self, request):
        user_data = request.data.get('user', {})
        serializer = UserRegistrationSerializer(data=user_data)
        
        if serializer.is_valid():
            try:
                user = UserService.create_user(**serializer.validated_data)
                user_serializer = UserSerializer(user)
                
                return Response(
                    {'user': user_serializer.data}, 
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return ResponseUtils.error_response(
                    message="Registration failed",
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return ResponseUtils.validation_error_response(serializer.errors)


class UserLoginView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [LoginRateThrottle]
    
    def post(self, request):
        user_data = request.data.get('user', {})
        serializer = UserLoginSerializer(data=user_data)
        
        if serializer.is_valid():
            try:
                user = UserService.authenticate_user(
                    email=serializer.validated_data['email'],
                    password=serializer.validated_data['password']
                )
                user_serializer = UserSerializer(user)
                
                return Response(
                    {'user': user_serializer.data}, 
                    status=status.HTTP_200_OK
                )
            except ValueError as e:
                return ResponseUtils.error_response(
                    message=str(e),
                    status_code=status.HTTP_401_UNAUTHORIZED
                )
        
        return ResponseUtils.validation_error_response(serializer.errors)


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data})
    
    def put(self, request):
        user_data = request.data.get('user', {})
        serializer = UserUpdateSerializer(
            request.user, 
            data=user_data, 
            partial=True
        )
        
        if serializer.is_valid():
            try:
                user = UserService.update_user(
                    request.user, 
                    **serializer.validated_data
                )
                user_serializer = UserSerializer(user)
                
                return Response({'user': user_serializer.data})
            except Exception as e:
                return ResponseUtils.error_response(
                    message="Profile update failed",
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return ResponseUtils.validation_error_response(serializer.errors)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'username'
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post', 'delete']

    def get_permissions(self):
        if self.action == 'follow':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        return Response({'profile': serializer.data})
    
    @action(
        detail=True, 
        methods=['post', 'delete'], 
        url_path='follow', 
        permission_classes=[IsAuthenticated]
    )
    def follow(self, request, username=None):
        profile = self.get_object()
        user = request.user
        
        if user == profile:
            return ResponseUtils.error_response(
                message=CANNOT_FOLLOW_YOURSELF,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            if request.method == 'POST':
                UserService.follow_user(user, profile)
            elif request.method == 'DELETE':
                UserService.unfollow_user(user, profile)
            
            serializer = ProfileSerializer(profile, context={'request': request})
            return Response({'profile': serializer.data})
            
        except Exception as e:
            return ResponseUtils.error_response(
                message="Follow operation failed",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
