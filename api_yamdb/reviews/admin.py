from django.contrib import admin

from .models import Title, Category, Genre, Review, Comment


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'score', 'title')
    empty_value_display = '-пусто-'
    ordering = ('-pk',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'review')
    empty_value_display = '-пусто-'
    ordering = ('-pk',)


class GenreInline(admin.TabularInline):
    model = Title.genre.through
    extra = 1


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    inlines = (GenreInline,)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass
