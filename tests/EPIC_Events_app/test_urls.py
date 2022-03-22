import pytest
from django.urls import reverse, resolve

from authentication.views import UserListView, UserRetrieveView


class TestUserUrls:
    def test_users_list_view(self):
        """
        Testing if the 'users' route is mapping to UserListView
        """

        url = reverse('users')
        assert resolve(url).view_name == "users"
        assert resolve(url).func.view_class == UserListView

    def test_user_details_view(self):
        """
        Testing if the 'user' route is mapping to UserRetrieveView
        """

        url = reverse('user', args="1")
        assert resolve(url).view_name == "user"
        assert resolve(url).func.view_class == UserRetrieveView
