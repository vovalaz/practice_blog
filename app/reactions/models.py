from django.db import models


class Reaction(models.Model):
    reaction_code = models.CharField(max_length=2, unique=True)
    emoji_image = models.ImageField(upload_to="media/emoji/", null=True)
