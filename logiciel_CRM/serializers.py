from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User as Auth_User
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Auth_User
        fields = ('username', 'password', 'password2')
        extra_kwargs = {'username': {'required': True}, 'password': {'required': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        auth_user = Auth_User.objects.create(username=validated_data['username'])
        auth_user.set_password(validated_data['password'])
        auth_user.save()
        user = Users.objects.create(email=auth_user.email, first_name=auth_user.first_name, user=auth_user,
                                    last_name=auth_user.last_name, password=auth_user.password, id=auth_user.id)
        user.save()
        return auth_user



# email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=Auth_User.objects.all())])
