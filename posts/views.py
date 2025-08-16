from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from rest_framework import generics, permissions, viewsets, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import Post, Like, Comment
from .serializers import (
    RegisterSerializer,
    PostSerializer,
    LikeSerializer,
    CommentSerializer,
    PostWithStatsSerializer
)
from .permissions import IsAuthorOrReadOnly


# -----------------------------
# User Registration
# -----------------------------
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# -----------------------------
# Posts
# -----------------------------
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'author__username']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'title']


# -----------------------------
# Likes
# -----------------------------
class LikePostAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response({'detail': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(LikeSerializer(like).data, status=status.HTTP_201_CREATED)

    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like_qs = Like.objects.filter(user=request.user, post=post)
        if like_qs.exists():
            like_qs.delete()
            return Response({'detail': 'Unliked'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Like not found'}, status=status.HTTP_404_NOT_FOUND)


# -----------------------------
# Comments
# -----------------------------
class CommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'])

    def perform_create(self, serializer):
        serializer.save(
            post_id=self.kwargs['post_id'],
            user=self.request.user   # ✅ fixed (use user, not author)
        )


class CommentDeleteAPIView(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # ✅ ensures only the user's own comment AND matches post_id
        return Comment.objects.filter(
            user=self.request.user,
            post_id=self.kwargs['post_id']
        )


# -----------------------------
# Posts with Stats
# -----------------------------
class PostListWithStatsAPIView(generics.ListAPIView):
    serializer_class = PostWithStatsSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # Prefetch only latest 3 comments globally (not per post)
        recent_comments_qs = Comment.objects.order_by('-created_at')[:3]
        return (
            Post.objects
            .all()
            .prefetch_related(
                Prefetch('comments', queryset=recent_comments_qs, to_attr='recent_comments')
            )
            .select_related('author')
        )
