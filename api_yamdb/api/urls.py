from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import TitleView, GenreView, CategoryView

app_name = 'api'

router_v1 = SimpleRouter()

router_v1.register(
    'titles',
    TitleView,
    basename='titles'
)

router_v1.register(
    'genres',
    GenreView,
    basename='genres'
)

router_v1.register(
    'categories',
    CategoryView,
    basename='categories'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]