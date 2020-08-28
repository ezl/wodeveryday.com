from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from core.gym.models import Gym


class GymDetails(models.Model):
    gym = models.OneToOneField(
        Gym,
        on_delete=models.PROTECT,
        primary_key=True,
    )
    gym_details_api_id = models.TextField()
    data = JSONField()

    def __str__(self):
        return ""

    class Meta:
        db_table = 'core_gymdetails'
