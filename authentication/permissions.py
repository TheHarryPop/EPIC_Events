from rest_framework.permissions import BasePermission, SAFE_METHODS

from logiciel_CRM.models import Contract, Event


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
            if obj.sales_staff == request.user:
                return True
            return False
        elif request.user.role == "Management":
            return True
        return False


class ContractsPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.user.role == "Support":
            return request.method in SAFE_METHODS
        return True

    def has_object_permission(self, request, view, obj):
        if request.user == obj.sales_staff:
            return True
        elif request.user.role == "Management":
            return True
        return False


class EventsPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.user.role == "Support":
            return request.method in SAFE_METHODS
        return True

    def has_object_permission(self, request, view, obj):
        if request.user == obj.support_staff:
            return True
        elif request.user.role == "Management":
            return True
        return False
