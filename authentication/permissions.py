from rest_framework.permissions import BasePermission, SAFE_METHODS

from logiciel_CRM.models import Customer, Contract, Event


class CustomersPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.user.role == "Support":
            return request.method in SAFE_METHODS
        return True

    def has_object_permission(self, request, view, obj):
        event = Event.objects.filter(support_staff=request.user, customer=obj)
        if request.user.role == "Support":
            if event:
                return request.method in SAFE_METHODS
            return False
        elif request.user.role == "Sales":
            if obj.sales_staff.id == request.user.id:
                return True
            return False
        elif request.user.role == "Management":
            return True


class ContractsPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            customer = Customer.objects.get(id=int(request.data['customer']))
            if customer.sales_staff != request.user:
                return False
        if request.user.role == "Support":
            return request.method in SAFE_METHODS
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.id == obj.sales_staff.id:
            return True
        elif request.user.role == "Management":
            return True
        return False


class EventsPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            customer = Customer.objects.get(id=int(request.data['customer']))
            if request.user.role == "Support":
                return request.method in SAFE_METHODS
            if customer.sales_staff != request.user:
                return False
        return True

    def has_object_permission(self, request, view, obj):
        customer = Customer.objects.get(id=str(obj.customer.id))
        if request.user.id == obj.support_staff.id or request.user.id == customer.sales_staff.id:
            return True
        elif request.user.role == "Management":
            return True
        return False
