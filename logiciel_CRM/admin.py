from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Customer, Contract, Event
from .forms import CustomerCreationForm, ContractCreationForm, EventCreationForm


class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    form = CustomerCreationForm

    list_display = ['sales_staff', 'name', 'surname', 'email', 'phone', 'mobile', 'company_name', 'date_created']


admin.site.register(Customer, CustomerAdmin)


class ContractAdmin(admin.ModelAdmin):
    model = Contract
    form = ContractCreationForm

    list_display = ['customer', 'sales_staff', 'amount', 'status', 'payment_due']


admin.site.register(Contract, ContractAdmin)


class EventAdmin(admin.ModelAdmin):
    model = Event
    form = EventCreationForm

    list_display = ['customer', 'support_staff', 'status', 'event_date', 'attendees', 'notes']


admin.site.register(Event, EventAdmin)
