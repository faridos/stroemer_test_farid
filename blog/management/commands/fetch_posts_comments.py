from django.core.management.base import BaseCommand
import time
from blog.api_client import APIClient
from blog.models import Post, Comment


class Command(BaseCommand):
    help = 'Fetch posts and comments from an API and insert them into the database'

    def handle(self, *args, **options):
        start_time = time.time()
        # Instantiate the APIClient with the base URL of the API
        api_client = APIClient(base_url='https://jsonplaceholder.typicode.com/')

        # Fetch posts from the API
        posts_data = api_client.get('posts')

        # Fetch comments from the API
        comments_data = api_client.get('posts/{post_id}/comments')

        # Insert posts into the database
        for post_data in posts_data:
            post = Post.objects.update_or_create(
                title=post_data['title'],
                body=post_data['body'],
                user=post_data['userId'],
                defaults={
                    'title': post_data['title'],
                    'body': post_data['body'],
                    'user': post_data['userId']}
            )
            msg = f'Inserted post with ID {post[0].id}' if post[1] else f'Updated post with ID {post[0].id}'
            self.stdout.write(self.style.SUCCESS(msg))

        # Insert comments into the database
        for comment_data in comments_data:
            comment = Comment.objects.update_or_create(
                post_id=comment_data['postId'],
                name=comment_data['name'],
                email=comment_data['email'],
                body=comment_data['body'],
                defaults={
                    'post_id': comment_data['postId'],
                    'name': comment_data['name'],
                    'email': comment_data['email'],
                    'body': comment_data['body']
                }
            )
            # post is tuple, post[1] : created : boolean
            msg = f'Inserted comment with ID {comment[0].id}' if comment[1] else f'Updated comment with ID {comment[0].id}'
            self.stdout.write(self.style.SUCCESS(msg))
        end_time = time.time()
        print(f"Execution time: {end_time - start_time} seconds")

# from blog.api_client import APIClient
# from blog.models import Post, Comment
# from django.core.management.base import BaseCommand
# from channels.db import database_sync_to_async
# import asyncio
# import time
#
# class Command(BaseCommand):
#     help = 'Sync data from remote server to local database'
#
#     def handle(self, *args, **options):
#         start_time = time.time()
#         asyncio.run(self.sync_data())
#         end_time = time.time()
#         print(f"Execution time: {end_time - start_time} seconds")
#
#     async def sync_data(self):
#         api_client = APIClient(base_url='https://jsonplaceholder.typicode.com/')
#         posts = await api_client.get('posts')
#         comments = await api_client.get('comments')
#
#         # Fetch existing post ids and comment ids from the local database asynchronously
#         existing_post_ids = await self.get_existing_post_ids()
#         existing_comment_ids = await self.get_existing_comment_ids()
#
#         # Process posts
#         tasks = []
#         for post in posts:
#             if post['id'] not in existing_post_ids:
#                 tasks.append(self.save_post(post))
#         await asyncio.gather(*tasks)
#
#         # Process comments
#         tasks = []
#         for comment in comments:
#             if comment['id'] not in existing_comment_ids:
#                 tasks.append(self.save_comment(comment))
#         await asyncio.gather(*tasks)
#
#     @database_sync_to_async
#     def get_existing_post_ids(self):
#         return set(Post.objects.values_list('id', flat=True))
#
#     @database_sync_to_async
#     def get_existing_comment_ids(self):
#         return set(Comment.objects.values_list('id', flat=True))
#
#     @database_sync_to_async
#     def save_post(self, post):
#         # Save post to local database asynchronously
#         return Post.objects.create(
#             id=post['id'],
#             title=post['title'],
#             body=post['body'],
#             user=post['userId']
#         )
#
#     @database_sync_to_async
#     def save_comment(self, comment):
#         # Save comment to local database asynchronously
#         return Comment.objects.create(
#             id=comment['id'],
#             post_id=comment['postId'],
#             name=comment['name'],
#             email=comment['email'],
#             body=comment['body']
#         )
