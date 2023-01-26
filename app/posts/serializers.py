from rest_framework import serializers
from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'text_content', 'post_date', 'user_id']
        extra_kwargs = {'user_id': {'read_only': True}}
