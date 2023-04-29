from rest_framework import serializers

from reviews.models import Title, Genre, Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class GenreSerializerForTitle(serializers.PrimaryKeyRelatedField, GenreSerializer):
    pass


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializerForTitle(many=True, queryset=Genre.objects.all())

    class Meta:
        model = Title
        fields = '__all__'
