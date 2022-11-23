import random

from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from .filters import FilterForTitle
from .permissions import IsAdminModeratorOwnerOrReadOnly, IsAdminOrReadOnly
from .serializers import (
    CategorySerializer,
    CodeEmailSerializer,
    CommentSerializers,
    GenreSerializer,
    ReviewSerializers,
    TitleReadSerializer,
    TitleSerializer,
    TokenSerializer
)
from .viewsets import CreateDeleteListViewSet


class CategoryViewSet(CreateDeleteListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('$name',)


class GenreViewSet(CreateDeleteListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('$name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilterForTitle

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return TitleReadSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializers
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)

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
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        new_queryset = Comment.objects.filter(
            title=title_id, review=review_id)
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=User.objects.get(
            username=self.request.user), review_id=review.id,
            title_id=title_id)


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
        if serializer.is_valid():
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            if not User.objects.filter(email=email, username=username):
                serializer.save(email=email, confirmation_code=code_generator)
                code = code_generator

            send_mail(
                'confirmation code',
                code,
                'yambd@yambd.ru', [email, ],
            )
            return Response({"username": username,
                             "email": email}, status=status.HTTP_200_OK)
        elif User.objects.filter(email=serializer.data.get('email'),
                                 username=serializer.data.get('username')):
            code = User.objects.get(
                email=serializer.data.get('email'),
                username=serializer.data.get('username')
            ).confirmation_code
            send_mail(
                'confirmation code',
                code,
                'yambd@yambd.ru', [serializer.data['email'], ],
            )
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
