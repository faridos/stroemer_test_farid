"""
File: serializers.py
Author: Farid Maghraoui
Description: This file contains the tests for  fetch_data_command.
"""

from django.test import TestCase
from django.core.management import call_command
from unittest.mock import patch, MagicMock
from blog.models import Post, Comment


class APIClientMock:
    def __init__(self, base_url):
        pass

    def get(self, endpoint):
        if endpoint == 'posts':
            return [
                {'userId': 1, 'id': 1, 'title': 'Test Post 1', 'body': 'Body of Test Post 1'},
                {'userId': 2, 'id': 2, 'title': 'Test Post 2', 'body': 'Body of Test Post 2'},
            ]
        elif endpoint == 'comments':
            return [
                {'postId': 1, 'id': 1, 'name': 'John', 'email': 'john@example.com', 'body': 'Comment on Post 1'},
                {'postId': 2, 'id': 2, 'name': 'Jane', 'email': 'jane@example.com', 'body': 'Comment on Post 2'},
            ]


class CommandTestCase(TestCase):
    @patch('blog.api_client.APIClient', side_effect=APIClientMock)
    def test_handle_command(self, mock_api_client):
        call_command('fetch_posts_comments')

        # Check if posts are inserted into the database
        self.assertEqual(Post.objects.count(), 2)

        # Check if comments are inserted into the database
        self.assertEqual(Comment.objects.count(), 2)

        # Check if posts are inserted with correct data
        self.assertEqual(Post.objects.filter(title='Test Post 1').count(), 1)
        self.assertEqual(Post.objects.filter(title='Test Post 2').count(), 1)

        # Check if comments are inserted with correct data
        self.assertEqual(Comment.objects.filter(name='John').count(), 1)
        self.assertEqual(Comment.objects.filter(name='Jane').count(), 1)

    @patch('blog.api_client.APIClient', side_effect=APIClientMock)
    @patch('blog.models.Post.objects.create', side_effect=MagicMock(side_effect=Exception))
    def test_handle_command_post_creation_failure(self, mock_post_create, mock_api_client):
        with self.assertRaises(Exception):
            call_command('fetch_posts_comments')

    @patch('blog.api_client.APIClient', side_effect=APIClientMock)
    @patch('blog.models.Comment.objects.create', side_effect=MagicMock(side_effect=Exception))
    def test_handle_command_comment_creation_failure(self, mock_comment_create, mock_api_client):
        with self.assertRaises(Exception):
            call_command('fetch_posts_comments')
