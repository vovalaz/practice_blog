from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from users.models import CustomUser
from users.serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = (permissions.AllowAny, )
        if self.action in ("list", "retrieve"):
            permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
        elif self.action in ("update", "partial_update", "destroy"):
            permission_classes = (permissions.IsAdminUser, )

        return [permission() for permission in permission_classes]


class UserLogout(APIView):
    def post(self, request):
        refresh_token = RefreshToken(request.data.get('refresh_token', ''))
        if refresh_token:
            refresh_token.blacklist()

        return Response('Success', status=status.HTTP_200_OK)
