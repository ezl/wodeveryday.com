from rest_framework import routers
from quickstart.affiliate_leaderboard.view import AffiliateLeaderboardViewSet

affiliate_leaderboard_router = routers.DefaultRouter()
affiliate_leaderboard_router.register('affiliate_leaderboard', AffiliateLeaderboardViewSet, basename='affiliate_leaderboard')

