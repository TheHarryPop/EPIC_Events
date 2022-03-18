from django.urls import reverse, resolve

from authentication.views import UserListView, UserRetrieveView
from logiciel_CRM.views import CustomerViewSet, ContractViewSet, EventViewSet


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


# class TestCustomerUrls:
#     def test_customers_list_view(self):
#         """
#         Testing if the 'customer' route is mapping to CustomerListView
#         """
#
#         url = reverse('customer', args="1")
#         assert resolve(url).view_name == "customers"
#         assert resolve(url).func.view_class == CustomerViewSet

    # def test_user_details_view(self):
    #     """
    #     Testing if the 'user' route is mapping to UserRetrieveView
    #     """
    #
    #     url = reverse('user', args="1")
    #     assert resolve(url).view_name == "user"
    #     assert resolve(url).func.view_class == UserRetrieveView
