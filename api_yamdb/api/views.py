from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Category, Comment, Genre, Review, Title
from Users.models import User
from .permissions import IsAdminOrReadOnly
from .serializers import (
    CategorySerializer,
    CommentSerializers,
    GenreSerializer,
    TitleReadSerializer,
    TitleSerializer,
    ReviewSerializers
)
from .viewsets import CreateDeleteListViewSet


class CategoryViewSet(CreateDeleteListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    filterset_fields = ('$name',)


class GenreViewSet(CreateDeleteListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    filterset_fields = ('$name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'category__slug', 'genre__slug')

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return TitleReadSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializers
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        new_queryset = Review.objects.filter(
            title=title_id)
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        author = User.objects.get(username=self.request.user)
        serializer.save(author=author, title_id=title.id)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializers
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        new_queryset = Comment.objects.filter(
            title=title_id, review=review_id)
        return new_queryset

