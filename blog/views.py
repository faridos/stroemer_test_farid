"""
File: views.py
Author: Farid Maghraoui
Description: This file contains API views for managing posts and comments.
"""
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .tasks import sync_post_with_remote, sync_comment_with_remote


class CustomPageNumberPagination(PageNumberPagination):
    """
    Custom pagination class for controlling page size and maximum page size.
    """
    page_size = 5  # Number of items per page
    page_size_query_param = 'page_size'  # URL query parameter to specify page size
    max_page_size = 100  # Maximum number of items per page


class PostListCreateAPIView(generics.ListCreateAPIView):
    """
    API view for retrieving a list of posts or creating a new post.

    - GET: Retrieve a paginated list of posts.
    - POST: Create a new post.

    Pagination:
    This endpoint supports pagination. By default, it returns 5 items per page,
    with a maximum page size of 100.

    For creating a new post, the `title`, `body`, and `user` fields are required.
    """
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all().order_by('id')
    serializer_class = PostSerializer
    pagination_class = CustomPageNumberPagination

    def perform_create(self, serializer):
        """
        Perform creation of a new post.

        Sets the `user` field to the specific user ID provided by the assignment.

        Args:
            serializer: Serializer instance containing post data.
        """
        serializer.save(user=99999942)
        # Trigger synchronization task for creating a post
        sync_post_with_remote.delay(serializer.data, action="POST")


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting a specific post.

    - GET: Retrieve a specific post by ID.
    - PUT: Update a specific post by ID.
    - DELETE: Delete a specific post by ID.

    For updating a post, all fields can be modified.

    For deleting a post, the post will be permanently removed from the database.
    """
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_update(self, serializer):
        serializer.save()
        sync_post_with_remote.delay(serializer.data, action=self.request.method)

    def perform_destroy(self, instance):
        instance.delete()
        # Trigger synchronization task for deleting a comment
        sync_post_with_remote.delay(instance.id, action="DELETE")


class CommentListCreateAPIView(generics.ListCreateAPIView):
    """
    API view for retrieving a list of comments or creating a new comment.

    - GET: Retrieve a paginated list of comments.
    - POST: Create a new comment.

    Pagination:
    This endpoint supports pagination. By default, it returns 5 items per page,
    with a maximum page size of 100.

    For creating a new comment, the `post`, `name`, `email`, and `body` fields are required.
    """
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        """
        Get the queryset of comments.

        Filters the queryset by `post_id` if provided as a query parameter.

        Returns:
            Filtered queryset of comments.
        """
        queryset = Comment.objects.all().order_by('id')
        post_id = self.request.query_params.get('post_id')
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save()
        # Trigger synchronization task for creating a comment
        sync_comment_with_remote.delay(
            serializer.data,
            action="POST",
        )


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting a specific comment.

    - GET: Retrieve a specific comment by ID.
    - PUT: Update a specific comment by ID.
    - DELETE: Delete a specific comment by ID.

    For updating a comment, all fields can be modified.

    For deleting a comment, the comment will be permanently removed from the database.
    """
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_update(self, serializer):
        serializer.save()
        sync_comment_with_remote.delay(serializer.data, action=self.request.method)

    def perform_destroy(self, instance):
        instance.delete()
        # Trigger synchronization task for deleting a comment
        sync_comment_with_remote.delay(instance.id, action="DELETE")
