from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from posts.models import Post
from posts.serializers import PostSerializer, PostDetailSerializer
from posts.permissions import IsUserAuthorOrAdmin
from posts.models import PostReactions
from configs.collections import Actions


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().prefetch_related("post_reactions")
    serializer_class = PostSerializer

    def get_permissions(self):
        permission_classes = (permissions.AllowAny,)
        if self.action == "create":
            permission_classes = (permissions.IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            permission_classes = (IsUserAuthorOrAdmin,)

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == Actions.RETRIEVE:
            return PostDetailSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class ReactToPost(APIView):
    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def post(self, request: Request, *args, **kwargs) -> Response:
        reaction = request.data.get("reaction")
        obj, created = PostReactions.objects.get_or_create(
            user=request.user,
            post=Post.objects.get(id=self.kwargs["post"]),
            defaults={
                "reaction": reaction,
            }
        )

        if not created:
            if obj.reaction == reaction:
                obj.delete()
                return Response(f"Reaction {reaction} to post {obj.post} deleted", status=status.HTTP_204_NO_CONTENT)
            else:
                obj.reaction = reaction
                obj.save()
                return Response(f"Reaction {reaction} to post {obj.post} saved", status=status.HTTP_200_OK)

        return Response(f"Reaction {reaction} to post {obj.post} saved", status=status.HTTP_201_CREATED)
