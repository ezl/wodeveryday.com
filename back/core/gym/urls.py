from rest_framework import routers
from core.gym.views import GymViewSet

gym_router = routers.DefaultRouter()
gym_router.register('gyms', GymViewSet)

