from authentication.models import User
from logiciel_CRM.models import Customer, Contract, Event

import pytest


@pytest.fixture
def sales_staff():
    user = User.objects.create(username='TestSalesStaff', password='random_password', role='Sales')
    return user


@pytest.fixture
def support_staff():
    user = User.objects.create(username='TestSupportStaff', password='random_password', role='Support')
    return user


@pytest.fixture
def customer(sales_staff):
    customer = Customer.objects.create(sales_staff=sales_staff, name="Jean", surname="Michel",
                                       email="jean.mi@event.com", phone="0231659845", mobile="0606060606",
                                       company_name="event")
    return customer


@pytest.fixture
def contract(sales_staff, customer):
    contract = Contract.objects.create(sales_staff=sales_staff, customer=customer, amount=1000)
    return contract


@pytest.fixture
def event(customer, support_staff):
    event = Event.objects.create(customer=customer, support_staff=support_staff, event_date='2022-05-10 9:00',
                                 attendees=1, notes="RAS")
    return event


class TestCustomersModels:

    @pytest.mark.django_db
    def test_customer_str(self, customer):
        """
        Testing whether Customer's __str__ method is implemented properly
        """
        assert customer.__str__() == f"Client: {customer.surname} | Company: {customer.company_name}"

    @pytest.mark.django_db
    def test_create_customer(self, sales_staff):
        """
        Testing if we can register a customer in DB
        """
        nbr_of_customers_before_add = Customer.objects.count()
        new_customer = Customer.objects.create(sales_staff=sales_staff, name="Jean", surname="Michel",
                                               email="jean.mi@event.com", phone="0255", mobile="0606060656",
                                               company_name="event")
        new_customer.save()
        nbr_of_customers_after_add = Customer.objects.count()
        assert (nbr_of_customers_after_add == nbr_of_customers_before_add + 1)


class TestContractsModels:

    @pytest.mark.django_db
    def test_contract_str(self, contract):
        """
        Testing whether Contract's __str__ method is implemented properly
        """
        assert contract.__str__() == f"Client: {contract.customer} | Sign: {contract.status} | Sales Staff:" \
                                     f" {contract.sales_staff}"

    @pytest.mark.django_db
    def test_create_contract(self, sales_staff, customer):
        """
        Testing if we can register a contract in DB
        """
        nbr_of_contracts_before_add = Contract.objects.count()
        new_contract = Contract.objects.create(sales_staff=sales_staff, customer=customer, amount=1500)
        new_contract.save()
        nbr_of_contracts_after_add = Contract.objects.count()
        assert (nbr_of_contracts_after_add == nbr_of_contracts_before_add + 1)


class TestEventsModels:

    @pytest.mark.django_db
    def test_event_str(self, event):
        """
        Testing whether Event's __str__ method is implemented properly
        """
        assert event.__str__() == f"Client: {event.customer} | Status: {event.status} | Support Staff:" \
                                  f" {event.support_staff}"

    @pytest.mark.django_db
    def test_create_event(self, support_staff, customer):
        """
        Testing if we can register a contract in DB
        """
        nbr_of_events_before_add = Event.objects.count()
        new_event = Event.objects.create(customer=customer, support_staff=support_staff, event_date='2022-05-11 22:00',
                                         attendees=1, notes="RAS")
        new_event.save()
        nbr_of_events_after_add = Event.objects.count()
        assert (nbr_of_events_after_add == nbr_of_events_before_add + 1)

