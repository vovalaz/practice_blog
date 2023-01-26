from django.urls import include, path
from rest_framework import routers

from posts import views


router = routers.DefaultRouter()
router.register("", views.PostViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("<int:post_id>/reaction/", views.ReactToPost.as_view()),
]
