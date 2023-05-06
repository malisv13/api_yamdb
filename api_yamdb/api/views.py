from rest_framework import viewsets

from .serializers import TitleSerializer, GenreSerializer, CategorySerializer
from reviews.models import Title, Genre, Category
from .mixins import CsvImportMixin


class TitleView(viewsets.ModelViewSet, CsvImportMixin):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filename_to_import = 'titles.csv'
    import_model = Title


class GenreView(viewsets.ModelViewSet, CsvImportMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filename_to_import = 'genre.csv'
    import_model = Genre


class CategoryView(viewsets.ModelViewSet, CsvImportMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filename_to_import = 'category.csv'
    import_model = Category
