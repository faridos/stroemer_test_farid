# from django.test import TestCase
# from django.core.management import call_command
# from unittest.mock import patch, MagicMock
# from blog.models import Post, Comment
#
#
# class APIClientMock:
#     def __init__(self, base_url):
#         pass
#
#     def get(self, endpoint):
#         if endpoint == 'posts':
#             return [
#                 {'userId': 1, 'id': 1, 'title': 'Test Post 1', 'body': 'Body of Test Post 1'},
#                 {'userId': 2, 'id': 2, 'title': 'Test Post 2', 'body': 'Body of Test Post 2'},
#             ]
#         elif endpoint == 'comments':
#             return [
#                 {'postId': 1, 'id': 1, 'name': 'John', 'email': 'john@example.com', 'body': 'Comment on Post 1'},
#                 {'postId': 2, 'id': 2, 'name': 'Jane', 'email': 'jane@example.com', 'body': 'Comment on Post 2'},
#             ]
#
#
# class CommandTestCase(TestCase):
#     @patch('blog.api_client.APIClient', side_effect=APIClientMock)
#     def test_handle_command(self, mock_api_client):
#         call_command('fetch_posts_comments')
#
#         # Check if posts are inserted into the database
#         self.assertEqual(Post.objects.count(), 2)
#
#         # Check if comments are inserted into the database
#         self.assertEqual(Comment.objects.count(), 2)
#
#         # Check if posts are inserted with correct data
#         self.assertEqual(Post.objects.filter(title='Test Post 1').count(), 1)
#         self.assertEqual(Post.objects.filter(title='Test Post 2').count(), 1)
#
#         # Check if comments are inserted with correct data
#         self.assertEqual(Comment.objects.filter(name='John').count(), 1)
#         self.assertEqual(Comment.objects.filter(name='Jane').count(), 1)
#
#     @patch('blog.api_client.APIClient', side_effect=APIClientMock)
#     @patch('blog.models.Post.objects.create', side_effect=MagicMock(side_effect=Exception))
#     def test_handle_command_post_creation_failure(self, mock_post_create, mock_api_client):
#         with self.assertRaises(Exception):
#             call_command('fetch_posts_comments')
#
#     @patch('blog.api_client.APIClient', side_effect=APIClientMock)
#     @patch('blog.models.Comment.objects.create', side_effect=MagicMock(side_effect=Exception))
#     def test_handle_command_comment_creation_failure(self, mock_comment_create, mock_api_client):
#         with self.assertRaises(Exception):
#             call_command('fetch_posts_comments')


from django.test import TestCase
from unittest.mock import patch
from blog.models import Post, Comment
from django.core.management import call_command
from io import StringIO


class SyncDataCommandTestCase(TestCase):
    @patch('blog.api_client.APIClient.get')
    def test_sync_data_command(self, mock_get):
        # Mock API response data
        mock_posts_response = [{'id': 1, 'userId': 1, 'title': 'Test Title', 'body': 'Test Body'}]
        mock_comments_response = [{'id': 1, 'postId': 1, 'name': 'Test Name', 'email': 'test@example.com', 'body': 'Test Comment Body'}]

        mock_get.side_effect = [
            mock_posts_response,
            mock_comments_response
        ]

        # Call the command
        out = StringIO()
        call_command('fetch_posts_comments', stdout=out)

        # Check if the command output contains expected messages
        self.assertIn('Inserted post with ID 1', out.getvalue())
        self.assertIn('Inserted comment with ID 1', out.getvalue())

        # Check if the Post and Comment objects were created/updated
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 1)

        post = Post.objects.first()
        self.assertEqual(post.id, 1)
        self.assertEqual(post.title, 'Test Title')
        self.assertEqual(post.body, 'Test Body')
        self.assertEqual(post.user, 1)

        comment = Comment.objects.first()
        self.assertEqual(comment.id, 1)
        self.assertEqual(comment.post_id, 1)
        self.assertEqual(comment.name, 'Test Name')
        self.assertEqual(comment.email, 'test@example.com')
        self.assertEqual(comment.body, 'Test Comment Body')

        # Reset mock state
        mock_get.reset_mock()

