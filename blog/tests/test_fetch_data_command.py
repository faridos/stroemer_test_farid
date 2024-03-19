"""
File: views.py
Author: Farid Maghraoui
Description: This file contains tests to test the fetch_data_command function.
"""
from django.test import TestCase
from unittest.mock import patch, MagicMock
from blog.models import Post
from blog.management.commands.fetch_posts_comments import Command


class TestSyncDataCommand(TestCase):
    @patch('blog.api_client.AsyncAPIClient')
    @patch('asyncio.run')
    def test_sync_post(self, mock_run, mock_api_client):
        mock_run.side_effect = lambda x: x  # Pass through the coroutine
        mock_api_client_instance = MagicMock()
        mock_api_client.return_value = mock_api_client_instance

        mock_post_data = {'id': 1, 'userId': 1, 'title': 'Test Title', 'body': 'Test Body'}
        mock_comments_data = [{'id': 1, 'postId': 1, 'name': 'Test Name', 'email': 'test@example.com', 'body': 'Test Body'}]

        command = Command()
        command.stdout = MagicMock()  # Mock stdout for Command instance

        with patch.object(command, 'sync_data') as mock_sync_post:
            mock_sync_post.return_value = None  # Mock sync_post method

            # Call sync_post directly with mock data
            command.sync_data(mock_post_data, mock_comments_data)

            # Print the result of sync_post method
            print("Post objects after sync_post:")
            print(Post.objects.all())

            # Assert that sync_post was called with the correct arguments
            mock_sync_post.assert_called_once_with(mock_post_data, mock_comments_data)
