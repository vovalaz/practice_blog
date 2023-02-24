from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from posts.models import Post
from posts.serializers import PostSerializer, PostReadOnlySerializer, PostDetailSerializer
from posts.permissions import IsAuthor
from posts.models import PostReactions
from configs.collections import Actions
from reactions.models import Reaction


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().prefetch_related("post_reactions__reaction").select_related("user")

    def get_permissions(self):
        permission_classes = (permissions.AllowAny,)
        if self.action == "create":
            permission_classes = (permissions.IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            permission_classes = (permissions.IsAdminUser | IsAuthor,)

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in (Actions.CREATE, Actions.UPDATE, Actions.PARTIAL_UPDATE, Actions.DESTROY):
            return PostSerializer
        if self.action == Actions.RETRIEVE:
            return PostDetailSerializer
        return PostReadOnlySerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReactToPost(APIView):
    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def post(self, request: Request, *args, **kwargs) -> Response:
        reaction = Reaction.objects.get(reaction_code=request.data.get("reaction"))
        obj, created = PostReactions.objects.get_or_create(
            user=request.user,
            post=Post.objects.get(id=self.kwargs["post"]),
            defaults={
                "reaction": reaction,
            },
        )
        response = {"reaction": reaction.reaction_code, "post": obj.post.title, }
        if not created:
            if obj.reaction == reaction:
                obj.delete()
                response.update({"status": "deleted", })
                return Response(response, status=status.HTTP_204_NO_CONTENT)
            else:
                obj.reaction = reaction
                obj.save()
                response.update({"status": "saved", })
                return Response(response, status=status.HTTP_200_OK)

        response.update({"status": "saved", })
        return Response(response, status=status.HTTP_201_CREATED)
