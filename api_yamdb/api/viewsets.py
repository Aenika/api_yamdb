from rest_framework import mixins, viewsets


class CreateDeleteListViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Создает вьюсет с методами: вернуть список, создать, удалить"""
    pass
