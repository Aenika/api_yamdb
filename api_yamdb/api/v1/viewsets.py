from rest_framework import mixins, viewsets


class CreateDeleteListViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """Создает вьюсет с методами: вернуть список, создать, удалить"""
    pass
