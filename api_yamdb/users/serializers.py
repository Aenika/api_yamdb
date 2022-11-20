from rest_framework import serializers

from .models import User


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = User


class MeUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = User
