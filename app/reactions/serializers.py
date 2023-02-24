from rest_framework import serializers
from reactions.models import Reaction


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ["id", "reaction_code", "emoji_image"]
