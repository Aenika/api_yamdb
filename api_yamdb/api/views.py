from rest_framework import viewsets

from reviews.models import Category, Genre, Title
from .permissions import IsAdminOrReadOnly
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer
)
from .viewsets import CreateDeleteListViewSet


class CategoryViewSet(CreateDeleteListViewSet):
    queryset = Category.objects.all
    serializer_class = CategorySerializer
    permission_classes = IsAdminOrReadOnly


class GenreViewSet(CreateDeleteListViewSet):
    queryset = Genre.objects.all
    serializer_class = GenreSerializer
    permission_classes = IsAdminOrReadOnly


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all
    serializer_class = TitleSerializer
    permission_classes = IsAdminOrReadOnly
