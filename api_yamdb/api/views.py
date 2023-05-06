from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.routers import DefaultRouter

from user.models import User

from .permissions import IsAdmin
from .serializers import (SignUpSerializer,
                          UserSerializer,
                          TokenSerializer,
                          TitleSerializer,
                          GenreSerializer,
                          CategorySerializer,
                          ReviewSerializer,
                          CommentSerializer)
from reviews.models import Title, Genre, Category, Review
from .mixins import CsvImportMixin
from .permissions import IsAuthorModeratorAdminOrReadOnly


class GetPostPatchDeleteViewSet(ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')


class ReviewViewSet(GetPostPatchDeleteViewSet):
    """Вьюсет для выполнения операций с объектами модели Review."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        serializer.save(author=self.request.user,
                        title=get_object_or_404(Title, pk=title_id))


class CommentViewSet(GetPostPatchDeleteViewSet):
    """Вьюсет для выполнения операций с объектами модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, title=title_id, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        serializer.save(author=self.request.user,
                        review=get_object_or_404(Review, pk=review_id,
                                                 title=title_id))


class TitleView(ModelViewSet, CsvImportMixin):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    filename_to_import = 'titles.csv'
    import_model = Title


class GenreView(ModelViewSet, CsvImportMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filename_to_import = 'genre.csv'
    import_model = Genre


class CategoryView(ModelViewSet, CsvImportMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filename_to_import = 'category.csv'
    import_model = Category


class SignupView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        email_body = (
            f'Здравствуйте, {user.username}.'
            f'\nКод подтверждения для доступа к API: {user.confirmation_code}.'
        )
        data = {
            'email_subject': 'Код подтверждения для доступа к API',
            'email_body': email_body,
            'to_email': user.email
        }
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(APIView):

     def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь не найден'},
                status=status.HTTP_404_NOT_FOUND)
        if data.get('confirmation_code') == user.confirmation_code:
            token = AccessToken.for_user(user)
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Ошибочный код подтверждения'},
            status=status.HTTP_400_BAD_REQUEST)
     

class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (SearchFilter, )
    search_fields = ('username', )

    @action(methods=['PATCH', 'GET'], detail=False,
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NotPutRouter(DefaultRouter):

    def get_method_map(self, viewset, method_map):
        bound_methods = super().get_method_map(viewset, method_map)
        if 'put' in bound_methods.keys():
            bound_methods.pop('put', None)
        return bound_methods
