from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import get_title_suggestions

from .views import (
    RegisterView,
    PostListCreateView,
    PostDetailView,
    LikePostAPIView,
    CommentListCreateAPIView,
    CommentDeleteAPIView,
    PostListWithStatsAPIView
)

urlpatterns = [
    # Authentication
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Posts
    path('posts/', PostListCreateView.as_view(), name='post_list_create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:post_id>/like/', LikePostAPIView.as_view(), name='like_post'),
    path('posts/<int:post_id>/comments/', CommentListCreateAPIView.as_view(), name='comment_list_create'),

    # Comments
    path('comments/<int:pk>/delete/', CommentDeleteAPIView.as_view(), name='comment_delete'),

    # Stats
    path('posts-with-stats/', PostListWithStatsAPIView.as_view(), name='posts_with_stats'),

    # Ai suggestions
    path("title-suggestions/", get_title_suggestions, name="title-suggestions"),
]
