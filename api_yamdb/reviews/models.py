from django.db import models


class Category(models.Model):

    name = models.CharField(
        'Наименование категории',
        max_length=150,
        blank=False,
        null=False
    )

    slug = models.SlugField(
        'Наименование категории slug',
        max_length=150,
        blank=False,
        null=False
    )


class Genre(models.Model):

    name = models.CharField(
        'Наименование жанра',
        max_length=150,
        blank=False,
        null=False
    )

    slug = models.SlugField(
        'Наименование жанра slug',
        max_length=150,
        blank=False,
        null=False
    )


class Title(models.Model):
    name = models.CharField(
        'Название произведения',
        max_length=150,
        blank=False,
        null=False
    )
    year = models.IntegerField(
        'Название произведения',
        default=1980,
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, related_name='titles')
    genre = models.ManyToManyField(Genre, related_name='titles', through="GenreTitle")


class GenreTitle(models.Model):
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE, null=False)
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE, null=False)
