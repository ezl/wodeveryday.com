import requests
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from quickstart.models import Affiliate
from quickstart.serializers import AffiliateSerializer


class AffiliateLeaderboardViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = ''
    serializer_class = []

    def list(self, request, *args, **kwargs):
        affiliate_name = request.query_params.get('affiliate_name')
        page = request.query_params.get('page', 1)
        affiliate_leaderboard_data = self.get_affiliate_leaderboard_data(affiliate_name, page)

        return Response(affiliate_leaderboard_data)

    def get_affiliate_leaderboard_data(self, affiliate_name, page):
        url = "https://games.crossfit.com/competitions/api/v1/competitions/open/2020/leaderboards/"
        affiliate_id = self.get_affiliate_id(affiliate_name)
        parameters = {
            "affiliate": affiliate_id,
            "division": 1,
            "scaled": 0,
            "page": page
        }

        r = requests.get(url=url, params=parameters)
        affiliate_leaderboard_data = r.json()

        return affiliate_leaderboard_data

    def get_affiliate_id(self, affiliate_name):
        url = "https://games.crossfit.com/competitions/api/v1/competitions/open/2020/affiliates"
        parameters = {
            "term": affiliate_name,
        }

        r = requests.get(url=url, params=parameters)
        data = r.json()
        affiliate_id = data[0].get('id')

        return affiliate_id


class AffiliateViewSet(mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):

    queryset = Affiliate.objects.all()
    serializer_class = AffiliateSerializer
