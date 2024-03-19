"""
File: serializers.py
Author: Farid Maghraoui
Description: This file contains the tests for the views.py file.
"""

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.reverse import reverse

from blog.models import Post, Comment
from myauth.models import FakeUser


class PostCRUDTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=FakeUser(id=99999942))
        self.post = Post.objects.create(title='Test Post', body='Test Body', user=99999942)

    def test_create_post(self):
        url = reverse('post-list-create')
        data = {'title': 'New Post', 'body': 'New Body', 'user': 99999942}
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.count(), 2)

    def test_retrieve_post(self):
        url = reverse('post-detail', kwargs={'pk': self.post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Test Post')

    def test_update_post(self):
        url = reverse('post-detail', kwargs={'pk': self.post.id})
        data = {'title': 'Updated Post about Strömer',
                'body': 'Strömer GmbH ist the monopole in Germany',
                'user': 99999942}
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Updated Post about Strömer')

    def test_delete_post(self):
        url = reverse('post-detail', kwargs={'pk': self.post.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Post.objects.count(), 0)


class CommentCRUDTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=FakeUser(id=99999942))
        self.post = Post.objects.create(title='Test ttt  ttt Post', body='Test test test Body', user=99999942)
        self.comment = Comment.objects.create(
            post=self.post,
            name='My name',
            email='test@stroemer.com',
            body='Test ttt Comment')

    def test_create_comment(self):
        data = {'post': self.post.id, 'name': 'New Name', 'email': 'new@example.com', 'body': 'New Comment'}
        url = reverse('comment-list-create')  # Assuming the URL name for creating comments is 'comment-list'
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.count(), 2)  # Assuming there's already a comment created in setUp

    def test_retrieve_comment(self):
        url = reverse('comment-detail', kwargs={'pk': self.comment.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'My name')

    def test_update_comment(self):
        url = reverse('comment-detail', kwargs={'pk': self.comment.id})
        data = {'name': 'Updated Name', 'email': 'updated@example.com', 'body': 'Updated Comment'}
        response = self.client.patch(url, data=data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Updated Name')

    def test_delete_comment(self):
        url = reverse('comment-detail', kwargs={'pk': self.comment.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Comment.objects.count(), 0)

    def test_list_comments_of_specific_post(self):
        """
        Test get all comments of specific post.
        becarefull with pagination, tests fail when pagination added
        ! the result.data does not work anymore, it should be response.data['results']
        ! post id is a query param instead, for decoupling.
        """
        url = reverse('comment-list-create')
        response = self.client.get(url, {'post': self.post.id})
        self.assertEqual(response.status_code, 200)
        # Assuming only one comment is created for the post
        self.assertEqual(len(response.data['results']), 1)
