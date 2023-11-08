from django.contrib.auth.mixins import UserPassesTestMixin

class UserCanDeletePostMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object().user

class UserCanUpdatePostMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object().user