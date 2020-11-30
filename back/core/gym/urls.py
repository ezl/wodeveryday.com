from rest_framework import routers
from core.gym.views import GymViewSet, GymLeaderboardViewSet, GymDetailsViewSet

router = routers.DefaultRouter()
router.register('gyms', GymViewSet)

router.register('gym_details', GymDetailsViewSet, basename='gym_details')

router.register('gym_leaderboard', GymLeaderboardViewSet, basename='gym_leaderboard')
