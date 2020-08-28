from rest_framework import serializers
from core.gym_leaderboard.models import GymLeaderboard


class GymLeaderboardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GymLeaderboard
        fields = [
            'id',
            'leaderboard_api_id',
            'data'
        ]
