from rest_framework import mixins, viewsets
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .decorators import is_admin
from .models import User
from .serializers import AdminUserSerializer, MeUserSerializer
from .permissions import IsAdmin


class AdminUsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class MeUser(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self, request):
        serializer = MeUserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = MeUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
