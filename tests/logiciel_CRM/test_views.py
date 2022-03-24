import pytest
from django.urls import reverse

from authentication.models import User
from logiciel_CRM.models import Customer, Contract, Event


class TestCustomerView:
    @pytest.mark.django_db
    def test_retrieve_customer_list(self, client):
        seller = User.objects.create_user(username='seller', password='1234azert', role='Sales')
        customer = Customer.objects.create(sales_staff=seller, name="Jean", surname="Michel",
                                           email="jean.mi@event.com", phone="0231659845", mobile="0606060606",
                                           company_name="event")
        response_login = client.post(reverse('login'), data={'username': 'seller', 'password': '1234azert'})
        token = response_login.data['access']
        response_details = client.get(reverse('customer-list'), HTTP_AUTHORIZATION=f'Bearer {token}')
        assert response_details.status_code == 200
        assert response_details.data['results'][0]['email'] == customer.email

    @pytest.mark.django_db
    def test_retrieve_customer_details_authorized_seller(self, client):
        seller = User.objects.create_user(username='seller', password='1234azert', role='Sales')
        customer = Customer.objects.create(sales_staff=seller, name="Jean", surname="Michel",
                                           email="jean.mi@event.com", phone="0231659845", mobile="0606060606",
                                           company_name="event")
        response_login = client.post(reverse('login'), data={'username': 'seller', 'password': '1234azert'})
        token = response_login.data['access']
        response_details = client.get(reverse('customer-detail', args=[customer.id]),
                                      HTTP_AUTHORIZATION=f'Bearer {token}')
        assert response_details.status_code == 200
        assert response_details.data['email'] == customer.email

    @pytest.mark.django_db
    def test_retrieve_customer_details_unauthorized_seller(self, client):
        seller = User.objects.create_user(username='seller', password='1234azert', role='Sales')
        seller2 = User.objects.create_user(username='seller2', password='1234azert', role='Sales')
        customer = Customer.objects.create(sales_staff=seller2, name="Jean", surname="Michel", email="jean.mi@event.com"
                                           , phone="0231659845", mobile="0606060606", company_name="event")
        response_login = client.post(reverse('login'), data={'username': 'seller', 'password': '1234azert'})
        token = response_login.data['access']
        response_details = client.get(reverse('customer-detail', args=[customer.id]),
                                      HTTP_AUTHORIZATION=f'Bearer {token}')
        assert response_details.status_code == 403
        assert 'You do not have permission' in response_details.data['detail']

    @pytest.mark.django_db
    def test_retrieve_customer_details_authorized_support(self, client):
        seller = User.objects.create_user(username='seller', password='1234azert', role='Sales')
        support = User.objects.create_user(username='support', password='1234azert', role='Support')
        customer = Customer.objects.create(sales_staff=seller, name="Jean", surname="Michel",
                                           email="jean.mi@event.com", phone="0231659845", mobile="0606060606",
                                           company_name="event")
        event = Event.objects.create(customer=customer, support_staff=support, event_date='2022-05-11 22:00',
                                     attendees=1, notes="RAS")
        response_login = client.post(reverse('login'), data={'username': 'support', 'password': '1234azert'})
        token = response_login.data['access']
        response_details = client.get(reverse('customer-detail', args=[customer.id]),
                                      HTTP_AUTHORIZATION=f'Bearer {token}')
        assert response_details.status_code == 200
        assert response_details.data['email'] == customer.email

    @pytest.mark.django_db
    def test_retrieve_customer_details_unauthorized_support(self, client):
        seller = User.objects.create_user(username='seller', password='1234azert', role='Sales')
        support = User.objects.create_user(username='support', password='1234azert', role='Support')
        support2 = User.objects.create_user(username='support2', password='1234azert', role='Support')
        customer = Customer.objects.create(sales_staff=seller, name="Jean", surname="Michel",
                                           email="jean.mi@event.com", phone="0231659845", mobile="0606060606",
                                           company_name="event")
        event = Event.objects.create(customer=customer, support_staff=support2, event_date='2022-05-11 22:00',
                                     attendees=1, notes="RAS")
        response_login = client.post(reverse('login'), data={'username': 'support', 'password': '1234azert'})
        token = response_login.data['access']
        response_details = client.get(reverse('customer-detail', args=[customer.id]),
                                      HTTP_AUTHORIZATION=f'Bearer {token}')
        assert response_details.status_code == 403
        assert 'You do not have permission' in response_details.data['detail']

    @pytest.mark.django_db
    def test_retrieve_customer_details_manager(self, client):
        seller = User.objects.create_user(username='seller', password='1234azert', role='Sales')
        customer = Customer.objects.create(sales_staff=seller, name="Jean", surname="Michel",
                                           email="jean.mi@event.com", phone="0231659845", mobile="0606060606",
                                           company_name="event")
        manager = User.objects.create_user(username='manager', password='1234azert', role='Management')
        response_login = client.post(reverse('login'), data={'username': 'manager', 'password': '1234azert'})
        token = response_login.data['access']
        response_details = client.get(reverse('customer-detail', args=[customer.id]),
                                      HTTP_AUTHORIZATION=f'Bearer {token}')
        assert response_details.status_code == 200
        assert response_details.data['email'] == customer.email

    @pytest.mark.django_db
    def test_create_customer_with_seller(self, client):
        seller = User.objects.create_user(username='seller', password='1234azert', role='Sales')
        response_login = client.post(reverse('login'), data={'username': 'seller', 'password': '1234azert'})
        token = response_login.data['access']
        response_create_customer = client.post(reverse('customer-list'), HTTP_AUTHORIZATION=f'Bearer {token}',
                                               data={'sales_staff': '19', 'name': "Jean", 'surname': "Michel",
                                                     'email': "jean.mi@event.com", 'phone': "0231659845", 'mobile':
                                                     "0606060606", 'company_name': "event"})
        assert response_create_customer.status_code == 200
        assert response_create_customer.data['email'] == "jean.mi@event.com"

    @pytest.mark.django_db
    def test_create_customer_with_support(self, client):
        support = User.objects.create_user(username='support', password='1234azert', role='Support')
        response_login = client.post(reverse('login'), data={'username': 'support', 'password': '1234azert'})
        token = response_login.data['access']
        response_create_customer = client.post(reverse('customer-list'), HTTP_AUTHORIZATION=f'Bearer {token}',
                                               data={'sales_staff': '19', 'name': "Jean", 'surname': "Michel",
                                                     'email': "jean.mi@event.com", 'phone': "0231659845", 'mobile':
                                                     "0606060606", 'company_name': "event"})
        assert response_create_customer.status_code == 403
        assert 'You do not have permission' in response_create_customer.data['detail']


class TestContractView:
    @pytest.mark.django_db
    def test_retrieve_contract_list(self, client):
        seller = User.objects.create_user(username='seller', password='1234azert', role='Sales')
        customer = Customer.objects.create(sales_staff=seller, name="Jean", surname="Michel",
                                           email="jean.mi@event.com", phone="0231659845", mobile="0606060606",
                                           company_name="event")
        contract = Contract.objects.create(sales_staff=seller, customer=customer, amount=1500)
        response_login = client.post(reverse('login'), data={'username': 'seller', 'password': '1234azert'})
        token = response_login.data['access']
        response_details = client.get(reverse('contract-list'), HTTP_AUTHORIZATION=f'Bearer {token}')
        assert response_details.status_code == 200
        assert response_details.data['results'][0]['amount'] == contract.amount

    @pytest.mark.django_db
    def test_retrieve_contract_details_authorized_seller(self, client):
        seller = User.objects.create_user(username='seller', password='1234azert', role='Sales')
        customer = Customer.objects.create(sales_staff=seller, name="Jean", surname="Michel",
                                           email="jean.mi@event.com", phone="0231659845", mobile="0606060606",
                                           company_name="event")
        contract = Contract.objects.create(sales_staff=seller, customer=customer, amount=1500)
        response_login = client.post(reverse('login'), data={'username': 'seller', 'password': '1234azert'})
        token = response_login.data['access']
        response_details = client.get(reverse('contract-detail', args=[contract.id]),
                                      HTTP_AUTHORIZATION=f'Bearer {token}')
        assert response_details.status_code == 200
        assert response_details.data['customer_surname'] == customer.surname

    @pytest.mark.django_db
    def test_retrieve_contract_details_unauthorized_seller(self, client):
        seller = User.objects.create_user(username='seller', password='1234azert', role='Sales')
        seller2 = User.objects.create_user(username='seller2', password='1234azert', role='Sales')
        customer = Customer.objects.create(sales_staff=seller2, name="Jean", surname="Michel", email="jean.mi@event.com"
                                           , phone="0231659845", mobile="0606060606", company_name="event")
        contract = Contract.objects.create(sales_staff=seller2, customer=customer, amount=1500)
        response_login = client.post(reverse('login'), data={'username': 'seller', 'password': '1234azert'})
        token = response_login.data['access']
        response_details = client.get(reverse('contract-detail', args=[contract.id]),
                                      HTTP_AUTHORIZATION=f'Bearer {token}')
        assert response_details.status_code == 403
        assert 'You do not have permission' in response_details.data['detail']

    @pytest.mark.django_db
    def test_retrieve_contract_details_support(self, client):
        seller = User.objects.create_user(username='seller', password='1234azert', role='Sales')
        support = User.objects.create_user(username='support', password='1234azert', role='Sales')
        customer = Customer.objects.create(sales_staff=seller, name="Jean", surname="Michel", email="jean.mi@event.com"
                                           , phone="0231659845", mobile="0606060606", company_name="event")
        contract = Contract.objects.create(sales_staff=seller, customer=customer, amount=1500)
        response_login = client.post(reverse('login'), data={'username': 'support', 'password': '1234azert'})
        token = response_login.data['access']
        response_details = client.get(reverse('contract-detail', args=[contract.id]),
                                      HTTP_AUTHORIZATION=f'Bearer {token}')
        assert response_details.status_code == 403
        assert 'You do not have permission' in response_details.data['detail']

    @pytest.mark.django_db
    def test_create_contract_authorized_seller(self, client):
        seller = User.objects.create_user(username='seller', password='1234azert', role='Sales')
        customer = Customer.objects.create(sales_staff=seller, name="Jean", surname="Michel", email="jean.mi@event.com"
                                           , phone="0231659845", mobile="0606060606", company_name="event")
        response_login = client.post(reverse('login'), data={'username': 'seller', 'password': '1234azert'})
        token = response_login.data['access']
        response_create_contract = client.post(reverse('contract-list'), HTTP_AUTHORIZATION=f'Bearer {token}',
                                               data={'sales_staff': seller.id, 'customer': customer.id,
                                                     'amount': 1500})
        assert response_create_contract.status_code == 200
        assert response_create_contract.data['customer_surname'] == customer.surname

    @pytest.mark.django_db
    def test_create_contract_unauthorized_seller(self, client):
        seller = User.objects.create_user(username='seller', password='1234azert', role='Sales')
        seller2 = User.objects.create_user(username='seller2', password='1234azert', role='Sales')
        customer = Customer.objects.create(sales_staff=seller2, name="Jean", surname="Michel",
                                           email="jean.mi@event.com",  phone="0231659845", mobile="0606060606",
                                           company_name="event")
        response_login = client.post(reverse('login'), data={'username': 'seller', 'password': '1234azert'})
        token = response_login.data['access']
        response_create_contract = client.post(reverse('contract-list'), HTTP_AUTHORIZATION=f'Bearer {token}',
                                               data={'sales_staff': seller2.id, 'customer': customer.id,
                                                     'amount': 1500})
        assert response_create_contract.status_code == 403
        assert 'You do not have permission' in response_create_contract.data['detail']

    @pytest.mark.django_db
    def test_retrieve_contract_details_manager(self, client):
        seller = User.objects.create_user(username='seller', password='1234azert', role='Sales')
        customer = Customer.objects.create(sales_staff=seller, name="Jean", surname="Michel",
                                           email="jean.mi@event.com", phone="0231659845", mobile="0606060606",
                                           company_name="event")
        contract = Contract.objects.create(sales_staff=seller, customer=customer, amount=1500)
        manager = User.objects.create_user(username='manager', password='1234azert', role='Management')
        response_login = client.post(reverse('login'), data={'username': 'manager', 'password': '1234azert'})
        token = response_login.data['access']
        response_details = client.get(reverse('contract-detail', args=[contract.id]),
                                      HTTP_AUTHORIZATION=f'Bearer {token}')
        assert response_details.status_code == 200
        assert response_details.data['customer_surname'] == customer.surname

    @pytest.mark.django_db
    def test_create_contract_with_support(self, client):
        user = User.objects.create_user(username='seller', password='1234azert', role='Sales')
        User.objects.create_user(username='support', password='1234azert', role='Support')
        customer = Customer.objects.create(sales_staff=user, name="Jean", surname="Michel", email="jean.mi@event.com"
                                           , phone="0231659845", mobile="0606060606", company_name="event")
        response_login = client.post(reverse('login'), data={'username': 'support', 'password': '1234azert'})
        token = response_login.data['access']
        response_create_contract = client.post(reverse('contract-list'), HTTP_AUTHORIZATION=f'Bearer {token}',
                                               data={'sales_staff': user.id, 'customer': customer.id, 'amount': 1500})
        assert response_create_contract.status_code == 403
        assert 'You do not have permission' in response_create_contract.data['detail']


class TestEventView:
    @pytest.mark.django_db
    def test_retrieve_event_list(self, client):
        seller = User.objects.create_user(username='support', password='1234azert', role='Support')
        customer = Customer.objects.create(sales_staff=seller, name="Jean", surname="Michel",
                                           email="jean.mi@event.com", phone="0231659845", mobile="0606060606",
                                           company_name="event")
        event = Event.objects.create(customer=customer, support_staff=seller, event_date='2022-05-11 22:00',
                                    attendees=1,
                             notes="RAS")
        response_login = client.post(reverse('login'), data={'username': 'support', 'password': '1234azert'})
        token = response_login.data['access']
        response_details = client.get(reverse('event-list'), HTTP_AUTHORIZATION=f'Bearer {token}')
        assert response_details.status_code == 200
        assert response_details.data['results'][0]['customer_surname'] == customer.surname

    @pytest.mark.django_db
    def test_retrieve_event_details_authorized_seller(self, client):
        seller = User.objects.create_user(username='seller', password='1234azert', role='Sales')
        support = User.objects.create_user(username='support', password='1234azert', role='Support')
        customer = Customer.objects.create(sales_staff=seller, name="Jean", surname="Michel",
                                           email="jean.mi@event.com", phone="0231659845", mobile="0606060606",
                                           company_name="event")
        event = Event.objects.create(customer=customer, support_staff=support, event_date='2022-05-11 22:00',
                                     attendees=1, notes="RAS")
        response_login = client.post(reverse('login'), data={'username': 'seller', 'password': '1234azert'})
        token = response_login.data['access']
        response_details = client.get(reverse('event-detail', args=[event.id]),
                                      HTTP_AUTHORIZATION=f'Bearer {token}')
        assert response_details.status_code == 200
        assert response_details.data['customer_company_name'] == customer.company_name

    @pytest.mark.django_db
    def test_retrieve_contract_details_unauthorized_seller(self, client):
        seller = User.objects.create_user(username='seller', password='1234azert', role='Sales')
        seller2 = User.objects.create_user(username='seller2', password='1234azert', role='Sales')
        support = User.objects.create_user(username='support', password='1234azert', role='Support')
        customer = Customer.objects.create(sales_staff=seller2, name="Jean", surname="Michel",
                                           email="jean.mi@event.com", phone="0231659845", mobile="0606060606",
                                           company_name="event")
        event = Event.objects.create(customer=customer, support_staff=support, event_date='2022-05-11 22:00',
                                     attendees=1,
                                     notes="RAS")
        response_login = client.post(reverse('login'), data={'username': 'seller', 'password': '1234azert'})
        token = response_login.data['access']
        response_details = client.get(reverse('event-detail', args=[event.id]),
                                      HTTP_AUTHORIZATION=f'Bearer {token}')
        assert response_details.status_code == 403
        assert 'You do not have permission' in response_details.data['detail']

    @pytest.mark.django_db
    def test_retrieve_event_details_authorized_support(self, client):
        seller = User.objects.create_user(username='seller', password='1234azert', role='Sales')
        support = User.objects.create_user(username='support', password='1234azert', role='Support')
        customer = Customer.objects.create(sales_staff=seller, name="Jean", surname="Michel",
                                           email="jean.mi@event.com", phone="0231659845", mobile="0606060606",
                                           company_name="event")
        event = Event.objects.create(customer=customer, support_staff=support, event_date='2022-05-11 22:00',
                                     attendees=1, notes="RAS")
        response_login = client.post(reverse('login'), data={'username': 'support', 'password': '1234azert'})
        token = response_login.data['access']
        response_details = client.get(reverse('event-detail', args=[event.id]),
                                      HTTP_AUTHORIZATION=f'Bearer {token}')
        assert response_details.status_code == 200
        assert response_details.data['customer_company_name'] == customer.company_name

    @pytest.mark.django_db
    def test_retrieve_event_details_unauthorized_support(self, client):
        seller = User.objects.create_user(username='seller', password='1234azert', role='Sales')
        support = User.objects.create_user(username='support', password='1234azert', role='Support')
        support2 = User.objects.create_user(username='support2', password='1234azert', role='Support')
        customer = Customer.objects.create(sales_staff=seller, name="Jean", surname="Michel",
                                           email="jean.mi@event.com", phone="0231659845", mobile="0606060606",
                                           company_name="event")
        event = Event.objects.create(customer=customer, support_staff=support2, event_date='2022-05-11 22:00',
                                     attendees=1, notes="RAS")
        response_login = client.post(reverse('login'), data={'username': 'support', 'password': '1234azert'})
        token = response_login.data['access']
        response_details = client.get(reverse('event-detail', args=[event.id]),
                                      HTTP_AUTHORIZATION=f'Bearer {token}')
        assert response_details.status_code == 403
        assert 'You do not have permission' in response_details.data['detail']

    @pytest.mark.django_db
    def test_retrieve_event_details_manager(self, client):
        seller = User.objects.create_user(username='seller', password='1234azert', role='Sales')
        support = User.objects.create_user(username='support', password='1234azert', role='Support')
        customer = Customer.objects.create(sales_staff=seller, name="Jean", surname="Michel",
                                           email="jean.mi@event.com", phone="0231659845", mobile="0606060606",
                                           company_name="event")
        event = Event.objects.create(customer=customer, support_staff=support, event_date='2022-05-11 22:00',
                                     attendees=1, notes="RAS")
        manager = User.objects.create_user(username='manager', password='1234azert', role='Management')
        response_login = client.post(reverse('login'), data={'username': 'manager', 'password': '1234azert'})
        token = response_login.data['access']
        response_details = client.get(reverse('event-detail', args=[event.id]),
                                      HTTP_AUTHORIZATION=f'Bearer {token}')
        assert response_details.status_code == 200
        assert response_details.data['customer_company_name'] == customer.company_name

    @pytest.mark.django_db
    def test_create_event_authorized_seller(self, client):
        seller = User.objects.create_user(username='seller', password='1234azert', role='Sales')
        support = User.objects.create_user(username='support', password='1234azert', role='Support')
        customer = Customer.objects.create(sales_staff=seller, name="Jean", surname="Michel", email="jean.mi@event.com"
                                           , phone="0231659845", mobile="0606060606", company_name="event")
        response_login = client.post(reverse('login'), data={'username': 'seller', 'password': '1234azert'})
        token = response_login.data['access']
        response_create_event = client.post(reverse('event-list'), HTTP_AUTHORIZATION=f'Bearer {token}',
                                            data={"customer": customer.id, "support_staff": support.id,
                                                  "event_date": '2022-05-11 22:00', "attendees": "1", "notes": "RAS"})
        assert response_create_event.status_code == 200
        assert response_create_event.data['customer_company_name'] == customer.company_name

    @pytest.mark.django_db
    def test_create_event_unauthorized_seller(self, client):
        seller = User.objects.create_user(username='seller', password='1234azert', role='Sales')
        seller2 = User.objects.create_user(username='seller2', password='1234azert', role='Sales')
        support = User.objects.create_user(username='support', password='1234azert', role='Support')
        customer = Customer.objects.create(sales_staff=seller2, name="Jean", surname="Michel",
                                           email="jean.mi@event.com"
                                           , phone="0231659845", mobile="0606060606", company_name="event")
        response_login = client.post(reverse('login'), data={'username': 'seller', 'password': '1234azert'})
        token = response_login.data['access']
        response_create_event = client.post(reverse('event-list'), HTTP_AUTHORIZATION=f'Bearer {token}',
                                            data={"customer": customer.id, "support_staff": support.id,
                                                  "event_date": '2022-05-11 22:00', "attendees": "1", "notes": "RAS"})
        assert response_create_event.status_code == 403
        assert 'You do not have permission' in response_create_event.data['detail']

    @pytest.mark.django_db
    def test_create_event_with_support(self, client):
        seller = User.objects.create_user(username='seller', password='1234azert', role='Sales')
        support = User.objects.create_user(username='support', password='1234azert', role='Support')
        customer = Customer.objects.create(sales_staff=seller, name="Jean", surname="Michel", email="jean.mi@event.com"
                                           , phone="0231659845", mobile="0606060606", company_name="event")
        response_login = client.post(reverse('login'), data={'username': 'support', 'password': '1234azert'})
        token = response_login.data['access']
        response_create_event = client.post(reverse('event-list'), HTTP_AUTHORIZATION=f'Bearer {token}',
                                            data={"customer": customer.id, "support_staff": support.id,
                                                  "event_date": '2022-05-11 22:00', "attendees": "1", "notes": "RAS"})
        assert response_create_event.status_code == 403
        assert 'You do not have permission' in response_create_event.data['detail']
