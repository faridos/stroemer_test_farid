from django.core.management.base import BaseCommand
from blog.api_client import APIClient
from blog.models import Post, Comment


class Command(BaseCommand):
    help = 'Fetch posts and comments from an API and insert them into the database'

    def handle(self, *args, **options):
        # Instantiate the APIClient with the base URL of the API
        api_client = APIClient(base_url='https://jsonplaceholder.typicode.com/')

        # Fetch posts from the API
        posts_data = api_client.get('posts')

        # Fetch comments from the API
        comments_data = api_client.get('comments')

        # Insert posts into the database
        for post_data in posts_data:
            post = Post.objects.create(
                title=post_data['title'],
                body=post_data['body'],
                user=post_data['userId']
            )
            self.stdout.write(self.style.SUCCESS(f'Inserted post with ID {post.id}'))

        # Insert comments into the database
        for comment_data in comments_data:
            comment = Comment.objects.create(
                post_id=comment_data['postId'],
                name=comment_data['name'],
                email=comment_data['email'],
                body=comment_data['body']
            )
            self.stdout.write(self.style.SUCCESS(f'Inserted comment with ID {comment.id}'))
