from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import GenericViewSet, ModelViewSet


class ModelMixinSet(CreateModelMixin, ListModelMixin,
                    DestroyModelMixin, GenericViewSet):
    pass


class GetPostPatchDeleteMixinSet(ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')
