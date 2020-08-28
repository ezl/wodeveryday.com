from django.contrib import admin
from django.urls import path, include

from core.gym.urls import gym_router, gym_details_router, gym_leaderboard_router


urlpatterns = [
    path('', include(gym_router.urls)),
    path('', include(gym_leaderboard_router.urls)),
    path('', include(gym_details_router.urls)),
    path('admin/', admin.site.urls),
]
