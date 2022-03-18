from authentication.models import User
from logiciel_CRM.models import Customer, Contract, Event

import pytest


@pytest.fixture
def sales_staff():
    user = User.objects.create(username='TestUser', password='random_password')
    return user


@pytest.fixture
def customer(sales_staff):
    customer = Customer.objects.create(sales_staff=sales_staff, name="Jean", surname="Michel",
                                       email="jean.mi@event.com", phone="0231659845", mobile="0606060606",
                                       company_name="event")
    return customer


class TestCustomersModels:

    @pytest.mark.django_db
    def test_profile_str(self, customer):
        """
        Testing whether Profile's __str__ method is implemented properly
        """
        customer = customer
        assert customer.__str__() == f"Client: {customer.surname} | Company: {customer.company_name}"

    @pytest.mark.django_db
    def test_create_customer(self, customer):
        """
        Testing how many customers registered in DB
        """
        nbr_of_customers_before_add = Customer.objects.count()
        new_user = customer
        new_user.save()
        nbr_of_customers_after_add = Customer.objects.count()
        assert (nbr_of_customers_after_add == nbr_of_customers_before_add + 1)


class TestContractsModels:

    @pytest.mark.django_db
    def test_profile_str(self, sales_staff):
        """
        Testing whether Profile's __str__ method is implemented properly
        """
        customer = Customer.objects.create(sales_staff=sales_staff, name="Jean", surname="Michel",
                                           email="jean.mi@event.com", phone="0231659845", mobile="0606060606",
                                           company_name="event")
        assert customer.__str__() == f"Client: {customer.surname} | Company: {customer.company_name}"

    @pytest.mark.django_db
    def test_create_customer(self, sales_staff):
        """
        Testing how many customers registered in DB
        """
        nbr_of_customers_before_add = Customer.objects.count()
        new_user = Customer.objects.create(sales_staff=sales_staff, name="Jean", surname="Michel",
                                           email="jean.mi@event.com", phone="0231659845", mobile="0606060606",
                                           company_name="event")
        new_user.save()
        nbr_of_customers_after_add = Customer.objects.count()
        assert (nbr_of_customers_after_add == nbr_of_customers_before_add + 1)

