from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy


class Post(models.Model):
    title = models.CharField(max_length=200)
    text_content = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True, blank=True)
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


class PostReactions(models.Model):
    class ReactionType(models.TextChoices):
        LIKE = "LK", gettext_lazy("Like")
        DISLIKE = "DL", gettext_lazy("Dislike")

    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=2, choices=ReactionType.choices)

    class Meta:
        unique_together = (("user_id", "post_id"),)
