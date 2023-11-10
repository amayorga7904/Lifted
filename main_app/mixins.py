from django.contrib.auth.mixins import UserPassesTestMixin, AccessMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.views.generic import View
from django.shortcuts import render
from django.urls import reverse
from .models import Photo, Post
import boto3
import uuid
import os

class UserCanDeletePostMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object().user

class UserCanUpdatePostMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object().user

class UserIsPostAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        # Get the post_id from the URL parameters
        post_id = self.kwargs['post_id']
        
        # Check if the current user is the author of the post
        return self.request.user == Post.objects.get(pk=post_id).author