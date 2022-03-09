from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.views import UserListView, UserRetrieveView
from logiciel_CRM.views import CustomerViewSet, ContractViewSet, EventViewSet

customer_router = routers.SimpleRouter()
customer_router.register('customer', CustomerViewSet, basename='customer')

contract_router = routers.SimpleRouter()
contract_router.register('contract', ContractViewSet, basename='contract')

event_router = routers.SimpleRouter()
event_router.register('event', EventViewSet, basename='event')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('rest_framework.urls')),
    path('api/', include(customer_router.urls)),
    path('api/', include(contract_router.urls)),
    path('api/', include(event_router.urls)),
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('api/users/', UserListView.as_view(), name='users'),
    path('api/users/<pk>/', UserRetrieveView.as_view(), name='user')
]
