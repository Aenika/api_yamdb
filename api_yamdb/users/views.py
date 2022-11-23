from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .permissions import IsAdmin
from .serializers import AdminUserSerializer, MeUserSerializer


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
