from rest_framework import permissions
from rest_framework import viewsets
from reactions.serializers import ReactionSerializer
from reactions.models import Reaction


class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer
    permission_classes = [permissions.IsAdminUser]
