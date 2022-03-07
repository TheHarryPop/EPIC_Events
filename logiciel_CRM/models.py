from django.db import models

from authentication.models import User


class Customer(models.Model):
    sales_staff = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=64, null=False)
    surname = models.CharField(max_length=64, null=False)
    email = models.EmailField(null=False)
    phone = models.CharField(max_length=64, unique=True, null=False)
    mobile = models.CharField(max_length=64, unique=True, null=False)
    company_name = models.CharField(max_length=64, null=False)
    date_created = models.DateField()
    date_updated = models.DateField()


class Contract(models.Model):
    sales_staff = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE, null=False)
    date_created = models.DateField()
    date_updated = models.DateField()
    amount = models.FloatField()
    status = models.BooleanField()
    payment_due = models.DateField()


class EventStatus(models.Model):
    status_description = models.CharField(max_length=64)


class Event(models.Model):
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE, null=False)
    support_staff = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)
    event_status = models.ForeignKey(to=EventStatus, on_delete=models.CASCADE, null=False)
    event_date = models.DateField()
    date_created = models.DateField()
    date_updated = models.DateField()
    attendees = models.IntegerField()
    notes = models.CharField(max_length=2048)
