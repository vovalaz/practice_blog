from rest_framework import serializers
from posts.models import Post, PostReactions
from users.serializers import UserBaseInfoSerializer


class PostSerializer(serializers.ModelSerializer):
    user = UserBaseInfoSerializer()

    class Meta:
        model = Post
        fields = ["id", "title", "text_content", "user"]
        extra_kwargs = {"user": {"read_only": True}}


class PostReactionsSerializer(serializers.ModelSerializer):
    user = UserBaseInfoSerializer()

    class Meta:
        model = PostReactions
        fields = ["id", "user", "reaction"]


class PostDetailSerializer(PostSerializer):
    post_reactions = PostReactionsSerializer()

    class Meta(PostSerializer.Meta):
        fields = ["id", "title", "text_content", "post_date", "post_reactions"]
