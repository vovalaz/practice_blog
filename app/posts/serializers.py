from rest_framework import serializers
from posts.models import Post, PostReactions
from users.serializers import UserBaseInfoSerializer
from reactions.serializers import ReactionSerializer


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "text_content", "user"]
        extra_kwargs = {"user": {"read_only": True}}


class PostReadOnlySerializer(PostSerializer):
    user = UserBaseInfoSerializer()

    class Meta(PostSerializer.Meta):
        fields = ["id", "title", "text_content", "user"]


class PostReactionsSerializer(serializers.ModelSerializer):
    user = UserBaseInfoSerializer(read_only=True)
    reaction = ReactionSerializer(read_only=True)

    class Meta:
        model = PostReactions
        fields = ["id", "user", "reaction"]
        extra_kwargs = {"user": {"read_only": True}}


class PostDetailSerializer(PostSerializer):
    post_reactions = PostReactionsSerializer(many=True, read_only=True)
    user = UserBaseInfoSerializer(read_only=True)

    class Meta(PostSerializer.Meta):
        fields = ["id", "title", "text_content", "post_date", "user", "post_reactions"]
        extra_kwargs = {"post_reactions": {"read_only": True}}
