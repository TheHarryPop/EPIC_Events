from authentication.models import User

import pytest


class TestUsersModels:
    @pytest.mark.django_db
    def test_profile_str(self):
        """
        Testing whether Profile's __str__ method is implemented properly
        """
        user = User.objects.create(username='TestUser', password='random_password')
        assert user.__str__() == f"User: {user.username} | Role: {user.role}"

    @pytest.mark.django_db
    def test_create_customer(self):
        """
        Testing how many Users registered in DB
        """
        nbr_of_users_before_add = User.objects.count()
        new_user = User.objects.create(username='TestUser', password='random_password')
        new_user.save()
        nbr_of_users_after_add = User.objects.count()
        assert (nbr_of_users_after_add == nbr_of_users_before_add + 1)

