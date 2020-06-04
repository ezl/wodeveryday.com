from rest_framework import routers
from quickstart.affiliate.view import AffiliateViewSet

affiliate_router = routers.DefaultRouter()
affiliate_router.register('affiliates', AffiliateViewSet)

