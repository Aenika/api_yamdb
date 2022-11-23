from rest_framework import serializers

from .models import User


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['username', 'email', 'first_name', 'last_name',
                  'bio', 'role']
        model = User


class MeUserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['username', 'email', 'first_name', 'last_name',
                  'bio', 'role']
        model = User
        read_only_fields = ('role',)

    def validate(self, data):
        if self.context.get('username') == "me":
            raise serializers.ValidationError('Нельзя использовать данное имя')
        return data
