from django.urls import include, path
from rest_framework import routers

from reactions import views


router = routers.DefaultRouter()
router.register("", views.ReactionViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
