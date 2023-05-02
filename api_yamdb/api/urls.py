from rest_framework import routers
from django.urls import path, include

from .views import (ReviewViewSet,
                    CommentViewSet)


router_v1 = routers.DefaultRouter()
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='review')

app_name = 'api'

urlpatterns = [
    path('v1/', include(router_v1.urls))
]
