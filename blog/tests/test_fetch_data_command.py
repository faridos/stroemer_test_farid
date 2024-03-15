from django.core.management import call_command
from django.test import TestCase
from unittest.mock import patch
from blog.models import Post, Comment


class TestFetchDataCommand(TestCase):
    @patch('blog.management.commands.fetch_posts_comments.APIClient')
    def test_handle(self, MockAPIClient):
        # Mock API response data
        posts_data = [
            {'id': 1, 'title': 'Post 1', 'body': 'Body of Post 1', 'userId': 1},
            {'id': 2, 'title': 'Post 2', 'body': 'Body of Post 2', 'userId': 2}
        ]
        comments_data = [
            {'postId': 1, 'name': 'Comment 1', 'email': 'comment1@example.com', 'body': 'Body of Comment 1'},
            {'postId': 2, 'name': 'Comment 2', 'email': 'comment2@example.com', 'body': 'Body of Comment 2'}
        ]

        # Set up the mock APIClient
        mock_client_instance = MockAPIClient.return_value
        mock_client_instance.get.side_effect = [posts_data, comments_data]
        # Call the command while we have the context of the MagicMock to simulate APIClient as above
        call_command('fetch_posts_comments')

        # Check if posts and comments in DB
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(Comment.objects.count(), 2)
