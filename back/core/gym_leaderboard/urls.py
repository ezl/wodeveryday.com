from rest_framework import routers
from core.gym_leaderboard.view import GymLeaderboardViewSet

gym_leaderboard_router = routers.DefaultRouter()
gym_leaderboard_router.register('gym_leaderboard', GymLeaderboardViewSet, basename='gym_leaderboard')

