from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from posts.models import Post
from posts.serializers import PostSerializer
from posts.permissions import IsUserAuthorOrAdmin
from posts.models import PostReactions


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        permission_classes = (permissions.AllowAny,)
        if self.action == "create":
            permission_classes = (permissions.IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            permission_classes = (IsUserAuthorOrAdmin,)

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class ReactToPost(APIView):
    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def post(self, request: Request, *args, **kwargs) -> Response:
        PostReactions.objects.create(
            user_id=request.user,
            post_id=Post.objects.get(id=self.kwargs["post_id"]),
            reaction=request.data.get("reaction")
        )
        return Response("Reaction saved", status=status.HTTP_201_CREATED)
