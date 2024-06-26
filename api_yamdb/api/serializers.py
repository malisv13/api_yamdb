from rest_framework import serializers
from django.core.validators import RegexValidator
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from users.models import User
from titles.models import Genre, Category, Title
from reviews.models import Review, Comment


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        exclude = ('id',)
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        exclude = ('id',)
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведения."""
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(required=False)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        read_only_fields = ('id',)


class GetTitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True, slug_field='slug', queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_username(self, data):
        if (data is not None and data.lower() == 'me'):
            raise serializers.ValidationError(
                'Username должен иметь отличное значение от "me"'
            )
        return data


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[
        RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Неккоректно введён <username>',
            code='invalid_username'
        )
    ],
        max_length=150,
        required=True
    )

    def create(self, validated_data):
        try:
            instance = User.objects.get(
                username=validated_data.get('username')
            )
        except ObjectDoesNotExist:
            return User.objects.create(**validated_data)
        return instance

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Username cannot be "me"')
        return value

    class Meta:
        model = User
        fields = ('email', 'username')


class JWTTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=50,
        required=True
    )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')
    """Сериализатор для отзывов."""
    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate_score(self, value):
        if value > 10 or value <= 0:
            raise serializers.ValidationError('Проверьте оценку!')
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST' and Review.objects.filter(
            title=title, author=author
        ).exists():
            raise serializers.ValidationError(
                'Больше одного отзыва оставлять нельзя')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')
    """Сериализатор для комментариев."""

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
