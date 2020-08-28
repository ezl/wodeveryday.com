from rest_framework import routers
from core.gym.views import GymViewSet, GymLeaderboardViewSet, GymDetailsViewSet

gym_router = routers.DefaultRouter()
gym_router.register('gyms', GymViewSet)

gym_details_router = routers.DefaultRouter()
gym_details_router.register('gym_details', GymDetailsViewSet, basename='gym_details')

gym_leaderboard_router = routers.DefaultRouter()
gym_leaderboard_router.register('gym_leaderboard', GymLeaderboardViewSet, basename='gym_leaderboard')
