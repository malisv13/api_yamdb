from django.contrib import admin

from .models import Title, Category, Genre


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
