# from django.test import TestCase
#
# from .models import Customer
#
#
# class CustomerTestCase(TestCase):
#     def test_create_customer(self):
#         # Tester combien de customer enregistrés en DB
#         nbr_of_customers_before_add = Customer.objects.count()
#
#         # Ajouter un customer dans la DB
#         new_customer = Customer(sales_staff=3, name="Jean", surname="Michel", email="jean.mi@event.com",
#                                 phone="0231659845", mobile="0606060606", company_name="event")
#         new_customer.save()
#
#         # Tester si la DB contient le nouveau customer
#         nbr_of_customer_after_add = Customer.objects.count()
#
#         self.assertTrue(nbr_of_customer_after_add == nbr_of_customers_before_add + 1)
