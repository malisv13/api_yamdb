from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import TokenView, SignupView, UsersViewSet

app_name = 'api'

router_v1 = SimpleRouter()

router_v1.register(
    'users',
    UsersViewSet,
    basename='users'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/token/', TokenView.as_view(), name='get_token'),
    path('v1/auth/signup/', SignupView.as_view(), name='signup')
]
