import pytest
from django.urls import reverse

from authentication.models import User


class TestUserView:
    @pytest.mark.django_db
    def test_login_ok(self, client):
        User.objects.create_user(username='seller', password='1234azert')
        url = reverse('login')
        response = client.post(url, data={'username': 'seller', 'password': '1234azert'})
        assert response.status_code == 200
        assert 'access' in response.data

    @pytest.mark.django_db
    def test_login_nok(self, client):
        User.objects.create_user(username='seller', password='1234azert')
        url = reverse('login')
        response = client.post(url, data={'username': 'seller', 'password': '2'})
        assert response.status_code == 401
        assert 'No active' in response.data['detail']

    @pytest.mark.django_db
    def test_retrieve_users_list(self, client):
        User.objects.create_user(username='seller', password='1234azert')
        response_login = client.post(reverse('login'), data={'username': 'seller', 'password': '1234azert'})
        token = response_login.data['access']
        response_list = client.get(reverse('users'), HTTP_AUTHORIZATION=f'Bearer {token}')
        assert response_list.status_code == 200
        assert User.objects.count() == response_list.data['count']

    @pytest.mark.django_db
    def test_retrieve_user_details(self, client):
        User.objects.create_user(username='seller', password='1234azert', role='Sales')
        response_login = client.post(reverse('login'), data={'username': 'seller', 'password': '1234azert'})
        token = response_login.data['access']
        response_details = client.get(reverse('user', args="6"), HTTP_AUTHORIZATION=f'Bearer {token}')
        assert response_details.status_code == 200
        assert 'Sales' in response_details.data['role']


