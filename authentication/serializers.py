from rest_framework.serializers import ModelSerializer

from authentication.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'last_name', 'email', 'phone', 'mobile', 'date_created', 'date_updated']
