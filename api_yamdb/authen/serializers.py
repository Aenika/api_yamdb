from rest_framework import serializers

from .models import CodeEmail


class CodeEmailSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=False)

    class Meta:
        fields = '__all__'
        model = CodeEmail


class TokenSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=False)

    class Meta:
        fields = '__all__'
        model = CodeEmail
