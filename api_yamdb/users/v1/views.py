import random

from django.core.mail import send_mail
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from core.constants import YAMBD_EMAIL
from users.models import User
from .permissions import IsAdmin
from .serializers import (
    AdminUserSerializer,
    CodeEmailSerializer,
    MeUserSerializer,
    TokenSerializer
)


class AdminUsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    lookup_field = "username"

    def perform_create(self, serializer):
        if self.request.data.get('email'):
            return serializer.save()
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeUser(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        serializer = MeUserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = MeUserSerializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


class CheckCode(APIView):

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data['username']
        )
        code_sent = serializer.validated_data['confirmation_code']
        if user.confirmation_code != code_sent:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        return Response(
            {'token': str(refresh.access_token)},
            status=status.HTTP_200_OK
        )


class SendCode(APIView):

    def post(self, request):
        serializer = CodeEmailSerializer(data=request.data)
        code_generator = ''.join(
            [str(random.randint(0, 10)) for i in range(6)]
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        serializer.save(email=email, confirmation_code=code_generator)
        code = code_generator

        send_mail(
            'confirmation code',
            code,
            YAMBD_EMAIL, [email, ],
        )
        return Response({"username": username,
                         "email": email}, status=status.HTTP_200_OK)
