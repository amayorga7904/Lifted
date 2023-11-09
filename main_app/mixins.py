from django.contrib.auth.mixins import UserPassesTestMixin, AccessMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.views.generic import View
from django.shortcuts import render
from django.urls import reverse


class UserCanDeletePostMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object().user

class UserCanUpdatePostMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object().user

