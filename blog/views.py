from rest_framework import generics
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 5  # Number of items per page
    page_size_query_param = 'page_size'  # URL query parameter to specify page size
    max_page_size = 100  # Maximum number of items per page


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('id')
    serializer_class = PostSerializer
    pagination_class = CustomPageNumberPagination

    def perform_create(self, serializer):
        # Set the user field to the specific user ID provided by the assignment
        serializer.save(user=99999942)


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = Comment.objects.all().order_by('id')
        post_id = self.request.query_params.get('post_id')
        if post_id:
            queryset = queryset.filter(post_id=post_id)
            print("###################", len(queryset), queryset)
        return queryset


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
