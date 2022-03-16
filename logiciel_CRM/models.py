from django.db import models

from authentication.models import User


class Customer(models.Model):
    sales_staff = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False, related_name='customer_sales_staff')
    name = models.CharField(max_length=64, null=False)
    surname = models.CharField(max_length=64, null=False)
    email = models.EmailField(null=False)
    phone = models.CharField(max_length=64, unique=True, null=False)
    mobile = models.CharField(max_length=64, unique=True, null=False)
    company_name = models.CharField(max_length=64, null=False)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)


class Contract(models.Model):
    sales_staff = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False,
                                    related_name='contract_sales_staff')
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE, null=False,
                                 related_name='contract_customer')
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    amount = models.FloatField()
    status = models.BooleanField(default=False)
    payment_due = models.DateField(null=True)


class Event(models.Model):
    InProgress = 'IN PROGRESS'
    Ended = 'ENDED'

    StatusChoices = (
        (InProgress, 'In progress'),
        (Ended, 'Ended'),
    )

    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE, null=False, related_name='event_customer')
    support_staff = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False,
                                      related_name='event_support_staff')
    status = models.CharField(max_length=64, choices=StatusChoices, default=InProgress, verbose_name='status')
    event_date = models.DateTimeField()
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    attendees = models.IntegerField()
    notes = models.CharField(max_length=2048)
