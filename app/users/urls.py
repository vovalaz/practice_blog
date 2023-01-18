from django.urls import include, path
from rest_framework import routers
from users import views

router = routers.DefaultRouter()
router.register("", views.UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("logout/", views.UserLogout.as_view()),
]
