from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.constants import CHARS_FOR_CODE, CHARS_FOR_USERNAME
from users.models import User


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name',
                  'bio', 'role')
        model = User
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            )
        ]


class MeUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name',
                  'bio', 'role')
        model = User
        read_only_fields = ('role',)


class CodeEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate(self, data):
        if data['username'] == "me":
            raise serializers.ValidationError('Нельзя использовать данное имя')
        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=CHARS_FOR_USERNAME)
    confirmation_code = serializers.CharField(max_length=CHARS_FOR_CODE)
