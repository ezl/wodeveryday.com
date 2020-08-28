from rest_framework import routers
from core.gym_details.views import GymDetailsViewSet

gym_details_router = routers.DefaultRouter()
gym_details_router.register('gym_details', GymDetailsViewSet, basename='gym_details')

