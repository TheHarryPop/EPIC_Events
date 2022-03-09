from django.db import models

from authentication.models import User


class Customer(models.Model):
    sales_staff = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, related_name='customer_sales_staff')
    name = models.CharField(max_length=64, null=False)
    surname = models.CharField(max_length=64, null=False)
    email = models.EmailField(null=False)
    phone = models.CharField(max_length=64, unique=True, null=False)
    mobile = models.CharField(max_length=64, unique=True, null=False)
    company_name = models.CharField(max_length=64, null=False)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)


class Contract(models.Model):
    sales_staff = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True,
                                    related_name='contract_sales_staff')
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE, null=False,
                                 related_name='contract_customer')
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    amount = models.FloatField()
    status = models.BooleanField(default=False)
    payment_due = models.DateField(auto_now_add=True)


class EventStatus(models.Model):
    status_description = models.CharField(max_length=64)


class Event(models.Model):
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE, null=False, related_name='event_customer')
    support_staff = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True,
                                      related_name='event_support_staff')
    event_status = models.ForeignKey(to=EventStatus, on_delete=models.CASCADE, null=False, related_name='event_status')
    event_date = models.DateField()
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    attendees = models.IntegerField()
    notes = models.CharField(max_length=2048)
