from django.db import models
from django.contrib.auth import get_user_model

from reactions.models import Reaction


class Post(models.Model):
    title = models.CharField(max_length=200)
    text_content = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"title={self.title}, post date={self.post_date}"


class PostReactions(models.Model):
    user = models.ForeignKey(get_user_model(), related_name="post_reactions", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="post_reactions", on_delete=models.CASCADE)
    reaction = models.ForeignKey(Reaction, related_name="reaction", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["user", "post"]
