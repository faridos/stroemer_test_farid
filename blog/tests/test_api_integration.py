from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from blog.models import Post, Comment, FakeUser


class BlogApiTest(APITestCase):
    def setUp(self):
        self.user = FakeUser()  # Assuming you have a FakeUser class for testing purposes
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(title='Test Post', body='Test Body', user=1)
        self.comment = Comment.objects.create(
            post=self.post,
            name='Test Name',
            email='test@example.com',
            body='Test Body'
        )

    def test_post_list(self):
        url = reverse('post-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_detail(self):
        url = reverse('post-detail', args=[self.post.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_list(self):
        url = reverse('comment-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_detail(self):
        url = reverse('comment-detail', args=[self.comment.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_create(self):
        url = reverse('post-list-create')
        data = {'title': 'New Post', 'body': 'New Body', 'user': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

    def test_comment_create(self):
        url = reverse('comment-list-create')
        data = {'post': self.post.pk, 'name': 'New Name', 'email': 'new@example.com', 'body': 'New Comment'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)
