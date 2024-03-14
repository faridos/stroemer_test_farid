# urls.py

from django.urls import path
from .views import PostListCreateAPIView, PostRetrieveUpdateDestroyAPIView, CommentListCreateAPIView, CommentRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyAPIView.as_view(), name='post-detail'),

    path('comments/', CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentRetrieveUpdateDestroyAPIView.as_view(), name='comment-detail'),
]
