from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Customer, Contract, Event
from .serializers import CustomerListSerializer, CustomerDetailSerializer, ContractListSerializer, \
    ContractDetailSerializer, EventListSerializer, EventDetailSerializer
from authentication.models import User
from authentication.permissions import CustomersPermissions, ContractsPermissions, EventsPermissions


class CustomerViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated, CustomersPermissions]
    serializer_class = CustomerListSerializer
    detail_serializer_class = CustomerDetailSerializer

    def get_queryset(self):
        return Customer.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = CustomerDetailSerializer(data=request.data)
        serializer.is_valid()
        serializer.save(sales_staff=request.user.id)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()


class ContractViewSet(ModelViewSet):

    lookup_url_kwarg = 'contract'
    permission_classes = [IsAuthenticated, ContractsPermissions]
    serializer_class = ContractListSerializer
    detail_serializer_class = ContractDetailSerializer

    def get_queryset(self):
        return Contract.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = ContractDetailSerializer(data=request.data)
        customer = Customer.objects.get(id=int(request.data['customer']))
        if customer.sales_staff == request.user:
            request.data._mutable = True
            request.data['sales_staff'] = request.user.id
            request.data._mutable = False
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data)
        else:
            message = 'You are not in charge of this customer'
            return Response(message)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()


class EventViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated, EventsPermissions]
    serializer_class = EventListSerializer
    detail_serializer_class = EventDetailSerializer

    def get_queryset(self):
        return Event.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = EventDetailSerializer(data=request.data)
        customer = Customer.objects.get(id=int(request.data['customer']))
        if customer.sales_staff == request.user:
            serializer.is_valid()
            if 'event_date' in serializer.errors:
                message = 'respect the format : YYYY-MM-DD hh:mm'
                return Response(message)
            serializer.save()
            return Response(serializer.data)
        else:
            message = 'You are not in charge of this customer'
            return Response(message)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()



    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()
