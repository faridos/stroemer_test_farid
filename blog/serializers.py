"""
File: serializers.py
Author: Farid Maghraoui
Description: This file contains serializers for the Post and Comment models.
"""
from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):

    user = serializers.IntegerField(required=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'user']
        read_only_fields = ['user']  # not needed for creating the Post


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'name', 'email', 'body']
