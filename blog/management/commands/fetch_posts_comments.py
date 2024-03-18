from django.core.management.base import BaseCommand
import time
from blog.api_client import APIClient
from blog.models import Post, Comment
from multiprocessing import Pool

# #######################################ASYNC APPROACH#########################
# from blog.api_client import APIClient
# from blog.models import Post, Comment
# from django.core.management.base import BaseCommand
# from channels.db import database_sync_to_async
# import asyncio
# import time
#
# BASE_API_URL = 'https://jsonplaceholder.typicode.com/'
# api_client = APIClient(base_url=BASE_API_URL)
#
#
# async def process_comments(post_id):
#     comments = await api_client.get(f'posts/{post_id}/comments')
#     return comments
#
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
#         posts = await api_client.get('posts')
#         # Fetch comments concurrently using asyncio
#         comments_list = await asyncio.gather(*[process_comments(post['id']) for post in posts])
#         tasks = []
#         for post, post_comments in zip(posts, comments_list):
#             tasks.append(self.sync_post(post, post_comments))
#         await asyncio.gather(*tasks)
#
#     @database_sync_to_async
#     def sync_post(self, post_data, comments):
#         id = post_data['id']
#         title = post_data['title']
#         body = post_data['body']
#         user = post_data['userId']
#         post_obj, created = Post.objects.update_or_create(
#             id=id,
#             title=title,
#             body=body,
#             user=user,
#             defaults={'id': id, 'title': title, 'body': body, 'user': user},
#         )
#         msg = f'Inserted post with ID {post_obj.id}' if created else f'Updated post with ID {post_obj.id}'
#         self.stdout.write(self.style.SUCCESS(msg))
#
#         # Create or update comments for the post
#         for comment_data in comments:
#             comment_obj, created = Comment.objects.update_or_create(
#                 id=comment_data['id'],
#                 post_id=post_obj.id,
#                 name=comment_data['name'],
#                 email=comment_data['email'],
#                 body=comment_data['body'],
#                 defaults={
#                     'id': comment_data['id'],
#                     'post_id': post_obj.id,
#                     'name': comment_data['name'],
#                     'email': comment_data['email'],
#                     'body': comment_data['body']
#                 }
#             )
#             msg = f'Inserted comment with ID {comment_obj.id}' if created else f'Updated comment with ID {comment_obj.id}'
#             self.stdout.write(self.style.SUCCESS(msg))

BASE_URL = 'https://jsonplaceholder.typicode.com/'
api_client = APIClient(base_url=BASE_URL)


def fetch_comments(post_id):
    response = api_client.get(f'posts/{post_id}/comments')
    return response


class Command(BaseCommand):
    help = 'Fetch posts and comments from an API and insert them into the database'

    def handle(self, *args, **options):
        start_time = time.time()
        # Instantiate the APIClient with the base URL of the API
        # Fetch posts from the API
        posts_data = api_client.get('posts')

        with Pool(processes=4) as pool:  # Adjust the number of processes as needed
            comments_lists = pool.map(fetch_comments, [post['id'] for post in posts_data])
        for post_data, comments in zip(posts_data, comments_lists):
            id = post_data['id']
            title = post_data['title']
            body = post_data['body']
            user = post_data['userId']
            post_obj, created = Post.objects.update_or_create(
                id=id,
                title=title,
                body=body,
                user=user,
                defaults={'id': id, 'title': title, 'body': body, 'user': user},
            )
            msg = f'Inserted post with ID {post_obj.id}' if created else f'Updated post with ID {post_obj.id}'
            self.stdout.write(self.style.SUCCESS(msg))

            # Create or update comments for the post
            for comment_data in comments:
                comment_obj, created = Comment.objects.update_or_create(
                    id=comment_data['id'],
                    post_id=post_obj.id,
                    name=comment_data['name'],
                    email=comment_data['email'],
                    body=comment_data['body'],
                    defaults={
                        'id': comment_data['id'],
                        'post_id': post_obj.id,
                        'name': comment_data['name'],
                        'email': comment_data['email'],
                        'body': comment_data['body']
                    }
                )
                msg = f'Inserted comment with ID {comment_obj.id}' if created else f'Updated comment with ID {comment_obj.id}'
                self.stdout.write(self.style.SUCCESS(msg))
        end_time = time.time()
        print(f"Execution time: {end_time - start_time} seconds")
