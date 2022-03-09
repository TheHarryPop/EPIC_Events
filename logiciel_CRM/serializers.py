from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Customer, Contract, Event


class CustomerListSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email']


class CustomerDetailSerializer(ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id', 'name', 'surname', 'email', 'phone', 'mobile', 'company_name', 'date_created',
                  'date_updated', 'sales_staff']


class ContractListSerializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = ['id', 'customer', 'date_created', 'amount']


class ContractDetailSerializer(ModelSerializer):
    customer_surname = serializers.ReadOnlyField(source='customer.surname')
    customer_email = serializers.ReadOnlyField(source='customer.email')

    class Meta:
        model = Contract
        fields = ['id', 'customer_surname', 'customer_email', 'date_created', 'date_updated', 'amount', 'status',
                  'payment_due', 'sales_staff']


class EventListSerializer(ModelSerializer):
    customer_surname = serializers.ReadOnlyField(source='customer.surname')
    customer_email = serializers.ReadOnlyField(source='customer.email')

    class Meta:
        model = Event
        fields = ['id', 'customer_surname', 'customer_email', 'event_date']


class EventDetailSerializer(ModelSerializer):
    customer_company_name = serializers.ReadOnlyField(source='customer.company_name')
    event_status_description = serializers.ReadOnlyField(source='event.status_description')

    class Meta:
        model = Event
        fields = ['id', 'customer_company_name', 'event_status_description', 'event_date',
                  'date_created', 'date_updated', 'attendees', 'notes']
