from rest_framework import serializers
from core.gym_details.models import GymDetails


class GymDetailsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GymDetails
        fields = [
            'id',
            'gym_details_api_id',
            'data'
        ]
