from rest_framework import routers
from core.gym.view import GymViewSet

gym_router = routers.DefaultRouter()
gym_router.register('gyms', GymViewSet)

