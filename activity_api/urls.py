from django.conf.urls import url, include
from .views import home, ActivityViewset, activity

from rest_framework import routers

router = routers.DefaultRouter()
router.register('activity', ActivityViewset, basename='activity')

urlpatterns = [
    url(r'^', include(router.urls)),
]
