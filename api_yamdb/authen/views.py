import random

from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import CodeEmailSerializer, CodeEmail, TokenSerializer
from users.models import User


class CheckCode(APIView):

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            if CodeEmail.objects.filter(code=serializer.validated_data['confirmation_code'],
                                        username=serializer.validated_data['username']).exists():
                user = User.objects.get(username=serializer.validated_data['username'])
                refresh = RefreshToken.for_user(user)
                return Response({'token': str(refresh.access_token)}, status=status.HTTP_200_OK)  # token
            else:
                return Response({'message': 'not equal'})
        else:
            return Response({'message': 'not valid'})


class SendCode(APIView):

    def post(self, request):
        serializer = CodeEmailSerializer(data=request.data)
        code_generator = ''.join([str(random.randint(0, 10)) for i in range(6)])
        if serializer.is_valid():
            email = serializer.validated_data['email']
            serializer.save(email=email, code=code_generator)
            send_mail('confirmation code', str(code_generator), 'yambd@yambd.ru', [email, ], )
            User.objects.get_or_create(email=serializer.validated_data['email'],
                                       username=serializer.validated_data['username'])
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
