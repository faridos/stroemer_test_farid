"""
File: serializers.py
Author: Farid Maghraoui
Description: This file contains the tests for our serializers module.
"""

from django.test import TestCase
from blog.models import Post, Comment
from blog.serializers import PostSerializer, CommentSerializer


class TestPostSerializer(TestCase):
    def test_valid_serializer_data(self):
        data = {'id': 1, 'title': 'Test Post', 'body': 'Test Body', 'user': 1}
        serializer = PostSerializer(data=data)
        self.assertTrue(serializer.is_valid())  # raise_exception=True incase  we wanna see the error

    def test_invalid_serializer_data(self):
        data = {'id': 2, 'title': 'Test Post', 'body': 'Test Body'}
        serializer = PostSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class TestCommentSerializer(TestCase):

    def setUp(self):
        self.post = Post.objects.create(title='Test Post', body='Test Body', user=1)

    def test_valid_serializer_data(self):
        data = {'id': 1, 'post': self.post.id, 'name': 'Test Name', 'email': 'test@example.com', 'body': 'Test Body'}
        serializer = CommentSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_serializer_data(self):
        data = {'name': 'Test Name', 'email': 'test@example.com', 'body': 'Test Body'}
        serializer = CommentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
