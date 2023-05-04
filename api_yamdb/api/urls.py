from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (TokenView,
                    SignupView,
                    UsersViewSet,
                    TitleView,
                    GenreView,
                    CategoryView,
                    CommentViewSet,
                    ReviewViewSet)

app_name = 'api'

router_v1 = SimpleRouter()

router_v1.register(
    'users',
    UsersViewSet,
    basename='users'
)

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

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/token/', TokenView.as_view(), name='get_token'),
    path('v1/auth/signup/', SignupView.as_view(), name='signup')
]
