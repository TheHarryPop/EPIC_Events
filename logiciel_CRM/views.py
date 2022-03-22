from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from django_filters import rest_framework as filters

from .models import Customer, Contract, Event
from .serializers import CustomerListSerializer, CustomerDetailSerializer, ContractListSerializer, \
    ContractDetailSerializer, EventListSerializer, EventDetailSerializer
from authentication.permissions import CustomersPermissions, ContractsPermissions, EventsPermissions


class CustomerViewSet(ModelViewSet):

    lookup_view_s = 'customer'
    permission_classes = [IsAuthenticated, CustomersPermissions]
    serializer_class = CustomerListSerializer
    detail_serializer_class = CustomerDetailSerializer
    queryset = Customer.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('surname', 'email')

    def create(self, request, *args, **kwargs):
        serializer = CustomerDetailSerializer(data=request.data)
        request.data._mutable = True
        request.data['sales_staff'] = request.user.id
        request.data._mutable = False
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CustomerDetailSerializer(data=request.data)
        if instance.sales_staff == request.user or request.user.role == 'Management':
            serializer.is_valid()
            serializer.update(instance=instance, validated_data=request.data)
            return Response(serializer.data)
        else:
            message = 'You are not in charge of this customer'
            return Response(message)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()


class ContractViewSet(ModelViewSet):

    lookup_url_kwarg = 'contract'
    permission_classes = [IsAuthenticated, ContractsPermissions]
    serializer_class = ContractListSerializer
    detail_serializer_class = ContractDetailSerializer
    queryset = Contract.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('customer__surname', 'customer__email', 'date_created', 'amount')

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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ContractDetailSerializer(data=request.data)
        if instance.customer.sales_staff == request.user or request.user.role == 'Management':
            if request.data['status'] == 'True':
                request.data._mutable = True
                request.data['payment_due'] = datetime.now().strftime("%Y-%m-%d")
                request.data._mutable = False
            serializer.is_valid()
            serializer.update(instance=instance, validated_data=request.data)
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
    queryset = Event.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('customer__surname', 'customer__email', 'event_date')

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
        serializer = EventDetailSerializer(data=request.data)
        if instance.customer.support_staff == request.user or request.user.role == 'Management':
            serializer.is_valid()
            if 'event_date' in serializer.errors:
                message = 'respect the format : YYYY-MM-DD hh:mm'
                return Response(message)
            serializer.update(instance=instance, validated_data=request.data)
            return Response(serializer.data)
        else:
            message = "You can't modify this event"
            return Response(message)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()
