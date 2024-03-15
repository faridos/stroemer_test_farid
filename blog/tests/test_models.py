from django.test import TestCase
from rest_framework.test import APIRequestFactory
from blog.models import Post, Comment
from blog.views import PostListCreateAPIView, PostRetrieveUpdateDestroyAPIView, CommentListCreateAPIView, CommentRetrieveUpdateDestroyAPIView


class PostCRUDTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.post = Post.objects.create(title='Test Post', body='Test Body', user=99999942)

    def test_create_post(self):
        data = {'title': 'New Post', 'body': 'New Body', 'user':99999942}
        request = self.factory.post('/posts/', data=data, format='json')
        view = PostListCreateAPIView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.count(), 2)  # Assuming there's already a post created in setUp

    def test_retrieve_post(self):
        request = self.factory.get(f'/posts/{self.post.id}/')
        view = PostRetrieveUpdateDestroyAPIView.as_view()
        response = view(request, pk=self.post.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Test Post')

    def test_update_post(self):
        data = {'title': 'Updated Post about Strömer',
                'body': 'Strömer GmbH ist the monopole in Germany',
                'user': 99999942}
        request = self.factory.put(f'/posts/{self.post.id}/', data=data)
        view = PostRetrieveUpdateDestroyAPIView.as_view()
        response = view(request, pk=self.post.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Updated Post about Strömer')

    def test_delete_post(self):
        request = self.factory.delete(f'/posts/{self.post.id}/')
        view = PostRetrieveUpdateDestroyAPIView.as_view()
        response = view(request, pk=self.post.id)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Post.objects.count(), 0)


class CommentCRUDTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.post = Post.objects.create(title='Test ttt  ttt Post', body='Test test test Body', user=99999942)
        self.comment = Comment.objects.create(
            post=self.post,
            name='My name',
            email='test@stroemer.com',
            body='Test ttt Comment')

    def test_create_comment(self):
        data = {'post': self.post.id, 'name': 'New Name', 'email': 'new@example.com', 'body': 'New Comment'}
        request = self.factory.post('/comments/', data=data, format='json')
        view = CommentListCreateAPIView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.count(), 2)  # Assuming there's already a comment created in setUp

    def test_retrieve_comment(self):
        request = self.factory.get(f'/comments/{self.comment.id}/')
        view = CommentRetrieveUpdateDestroyAPIView.as_view()
        response = view(request, pk=self.comment.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'My name')

    def test_update_comment(self):
        data = {'name': 'Updated Name', 'email': 'updated@example.com', 'body': 'Updated Comment'}
        request = self.factory.patch(f'/comments/{self.comment.id}/', data=data)
        view = CommentRetrieveUpdateDestroyAPIView.as_view()
        response = view(request, pk=self.comment.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Updated Name')

    def test_delete_comment(self):
        request = self.factory.delete(f'/comments/{self.comment.id}/')
        view = CommentRetrieveUpdateDestroyAPIView.as_view()
        response = view(request, pk=self.comment.id)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Comment.objects.count(), 0)

    def test_list_comments_of_specific_post(self):
        request = self.factory.get('/comments/', {'post_id': self.post.id})
        view = CommentListCreateAPIView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  # Assuming only one comment is created for the post