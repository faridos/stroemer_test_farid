"""
File: models.py
Author: Farid Maghraoui
Description: This file contains the models of the Post and Comment.
"""
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    user = models.PositiveIntegerField()  # just for the testing purpose

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()

    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"


class FakeUser:
    def __init__(self):
        self.is_authenticated = True
