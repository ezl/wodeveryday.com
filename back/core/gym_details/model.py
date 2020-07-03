from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from core.gym.model import Gym


class GymDetails(models.Model):
    gym = models.OneToOneField(
        Gym,
        on_delete=models.PROTECT,
        primary_key=True,
    )
    gym_details_api_id = models.TextField()
    data = JSONField()
    photos = ArrayField(
        models.ImageField(upload_to="gym_photos", blank=True, null=True),
        blank=True,
        null=True
    )

    def __str__(self):
        return ""
