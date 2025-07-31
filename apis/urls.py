from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, TagViewSet
from .views.user_views import ProfileViewSet, UserRegistrationView, UserLoginView, CurrentUserView

app_name = 'apis'

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'tags', TagViewSet)
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/users/', UserRegistrationView.as_view(), name='user-registration'),
    path('api/users/login/', UserLoginView.as_view(), name='user-login'),
    path('api/user/', CurrentUserView.as_view(), name='current-user'),
    path(
      'api/articles/<slug:slug>/comments/<int:comment_id>/',
      ArticleViewSet.as_view({'delete': 'delete_comment'}),
      name='article-comment-delete',
    ),
]
