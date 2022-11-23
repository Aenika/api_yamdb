from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CheckCode,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    SendCode,
    TitleViewSet
)

router_v1 = DefaultRouter()

router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

urlpatterns = [
    path('v1/auth/token/', CheckCode.as_view(), name='token'),
    path('v1/auth/signup/', SendCode.as_view(), name='signup'),
    path('v1/', include(router_v1.urls)),

]
