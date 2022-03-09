from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Customer, Contract, Event
from .serializers import CustomerListSerializer, CustomerDetailSerializer, ContractListSerializer, \
    ContractDetailSerializer, EventListSerializer, EventDetailSerializer


class CustomerViewSet(ModelViewSet):

    """
    permission_classes = [IsAuthenticated, CustomerPermissions]
    """
    serializer_class = CustomerListSerializer
    detail_serializer_class = CustomerDetailSerializer

    def get_queryset(self):
        return Customer.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = CustomerDetailSerializer(data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()


class ContractViewSet(ModelViewSet):

    """
    permission_classes = [IsAuthenticated, ContractPermissions]
    """
    serializer_class = ContractListSerializer
    detail_serializer_class = ContractDetailSerializer

    def get_queryset(self):
        return Contract.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = ContractDetailSerializer(data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()


class EventViewSet(ModelViewSet):

    """
    permission_classes = [IsAuthenticated, EventPermissions]
    """
    serializer_class = EventListSerializer
    detail_serializer_class = EventDetailSerializer

    def get_queryset(self):
        return Event.objects.all()

    """def create(self, request, *args, **kwargs):
        serializer = EventDetailSerializer(data=request.data)
        serializer.is_valid()
        event = serializer.save()"""

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()