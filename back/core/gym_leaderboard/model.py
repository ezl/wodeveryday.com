from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from core.gym.model import Gym


class GymLeaderboard(models.Model):
    leaderboard_api_id = models.IntegerField(blank=True, null=True)
    gym = models.OneToOneField(
        Gym,
        on_delete=models.PROTECT,
        primary_key=True,
    )
    data = ArrayField(
        JSONField()
    )

    def __str__(self):
        return ""
