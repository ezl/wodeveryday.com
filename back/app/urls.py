from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from quickstart.views import AffiliateViewSet, AffiliateLeaderboardViewSet

router = routers.DefaultRouter()
router.register('affiliates', AffiliateViewSet)
router.register('affiliate_leaderboard', AffiliateLeaderboardViewSet, basename='affiliate_leaderboard')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]
