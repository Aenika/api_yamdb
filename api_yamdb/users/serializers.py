from rest_framework import serializers

from .models import User


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = User
        exclude = ['id']


class MeUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = User
        read_only_fields = ('role',)

    def validate(self, data):
        if self.context['request'].user == "me":
            raise serializers.ValidationError('Нельзя использовать данное имя')
        return data
