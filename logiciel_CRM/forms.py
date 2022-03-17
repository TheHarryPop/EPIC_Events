from django import forms

from authentication.models import User
from .models import Customer, Contract, Event


class CustomerCreationForm(forms.ModelForm):
    sales_staff = forms.ModelChoiceField(queryset=User.objects.filter(role='Sales'))

    class Meta:
        model = Customer
        fields = ('name', 'surname', 'email', 'phone', 'mobile', 'company_name', 'sales_staff')


class ContractCreationForm(forms.ModelForm):
    customer = forms.ModelChoiceField(queryset=Customer.objects.all())
    sales_staff = forms.ModelChoiceField(queryset=User.objects.filter(role='Sales'))

    class Meta:
        model = Contract
        fields = ('customer', 'sales_staff', 'amount', 'status', 'payment_due')


class EventCreationForm(forms.ModelForm):
    customer = forms.ModelChoiceField(queryset=Customer.objects.all())
    support_staff = forms.ModelChoiceField(queryset=User.objects.filter(role='Support'))

    class Meta:
        model = Event
        fields = ('customer', 'support_staff', 'status', 'event_date', 'attendees', 'notes')
