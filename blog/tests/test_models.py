from django.test import TestCase
from django.db.utils import IntegrityError
from blog.models import Post, Comment


class TestPostModel(TestCase):
    def test_string_representation(self):
        post = Post.objects.create(title='gambary gambary!', body='Test Body', user=1)
        self.assertEqual(str(post), 'gambary gambary!')

    def test_post_creation(self):
        post = Post.objects.create(title='gambary gambary!', body='Test Body', user=1)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(post.title, 'gambary gambary!')

    def test_field_user_validations(self):
        # Missing required field (user)
        with self.assertRaises(IntegrityError):
            Post.objects.create(title='gambary gambary!', body='Test Body')


class TestCommentModel(TestCase):
    def test_string_representation(self):
        post = Post.objects.create(title='Test dummy post', body='Test Body', user=1)
        comment = Comment.objects.create(post=post, name='Farid Magh', email='farid@example.com', body='Test Body')
        self.assertEqual(str(comment), 'Comment by Farid Magh on Test dummy post')

    def test_comment_creation(self):
        post = Post.objects.create(title='Test Post', body='Test Body', user=1)
        comment = Comment.objects.create(post=post, name='Test Name', email='test@example.com', body='Test Body')
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(comment.post.title, 'Test Post')

    def test_comment_on_delete_cascade(self):
        post = Post.objects.create(title='Test Post', body='Test Body', user=1)
        Comment.objects.create(post=post, name='Test Name', email='test@example.com', body='Test Body')
        self.assertEqual(Comment.objects.count(), 1)

        # Deleting post also make sure to delete related comments
        post.delete()
        self.assertEqual(Comment.objects.count(), 0)

    # i can add more testing for field validations # TODO
