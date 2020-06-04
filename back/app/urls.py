from django.contrib import admin
from django.urls import path, include

from quickstart.affiliate.urls import affiliate_router
from quickstart.affiliate_leaderboard.urls import affiliate_leaderboard_router


urlpatterns = [
    path('', include(affiliate_router.urls)),
    path('', include(affiliate_leaderboard_router.urls)),
    path('admin/', admin.site.urls),
]
