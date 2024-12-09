from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'},
            }
        }

    # noinspection PyMethodMayBeStatic
    def validate_password(self, data):
        validate_password(data)
        return data

    def create(self, data):
        user = CustomUser.objects.create_user(**data)
        return user

    def update(self, instance, data):
        password = data.pop('password', None)
        user = super().update(instance, data)
        if password:
            user.set_password(password)
            user.save()
        return user
