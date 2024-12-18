from .models import CustomUser, Combatant, CombatantGroup, Group, Ambient
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
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


class CombatantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Combatant
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
        }

    def create(self, data):
        include_generative = data.get('include_generative', False)
        data['user'] = None if include_generative else self.context['request'].user
        return super().create(data)


class CombatantGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CombatantGroup
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class AmbientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ambient
        fields = '__all__'
