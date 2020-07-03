from django.contrib import admin
from django.urls import path, include

from core.gym.urls import gym_router
from core.gym_details.urls import gym_details_router
from core.gym_leaderboard.urls import gym_leaderboard_router


urlpatterns = [
    path('', include(gym_router.urls)),
    path('', include(gym_leaderboard_router.urls)),
    path('', include(gym_details_router.urls)),
    path('admin/', admin.site.urls),
]
