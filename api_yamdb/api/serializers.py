from rest_framework.serializers import (ModelSerializer,
                                        CharField,
                                        PrimaryKeyRelatedField,
                                        SlugRelatedField,
                                        ValidationError)

from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from user.models import User

from reviews.models import Title, Genre, Category, Review, Comment


class ReviewSerializer(ModelSerializer):
    author = SlugRelatedField(read_only=True,
                                          slug_field='username')
    """Сериализатор для отзывов."""
    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate_score(self, value):
        if value > 10 or value <= 0:
            raise ValidationError('Проверьте оценку!')
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST' and Review.objects.filter(
            title=title, author=author
        ).exists():
            raise ValidationError(
                'Больше одного отзыва оставлять нельзя')
        return data


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(read_only=True,
                                          slug_field='username')
    """Сериализатор для комментариев."""

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class GenreSerializerForTitle(PrimaryKeyRelatedField, GenreSerializer):
    pass


class TitleSerializer(ModelSerializer):
    genre = GenreSerializerForTitle(many=True, queryset=Genre.objects.all())

    class Meta:
        model = Title
        fields = '__all__'


class ModeratorOrAdminSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', 'email', 'bio', 'role')
        read_only_fields = ('role',)


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class SignUpSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = ('email', 'username')


class TokenSerializer(ModelSerializer):
    username = CharField(
        required=True
    )
    confirmation_code = CharField(
        required=True
    )

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )
