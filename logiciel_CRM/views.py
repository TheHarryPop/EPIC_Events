from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User as Auth_user

from .serializers import RegisterSerializer


class RegisterView(CreateAPIView):

    serializer_class = RegisterSerializer

    def get_queryset(self):
        queryset = Auth_user.objects.all()
        return queryset
