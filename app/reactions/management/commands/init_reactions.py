from django.core.management.base import BaseCommand
from configs.collections import ReactionTypes
from reactions.models import Reaction
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = "Initializes default values for reactions model with data from config/collections file"

    def handle(self, *args, **kwargs):
        for reaction in ReactionTypes:
            try:
                Reaction.objects.create(reaction_code=reaction.value)
                self.stdout.write(
                    self.style.SUCCESS(
                        "Reaction %s with code %s created successfully" % (reaction.name, reaction.value)
                    )
                )
            except IntegrityError:
                self.stdout.write(
                    self.style.WARNING(
                        "Unique restriction violated with %s reaction %s" % (reaction.name, reaction.value)
                    )
                )
