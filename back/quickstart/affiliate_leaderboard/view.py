from datetime import datetime

import requests
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from app.constants import GET_AFFILIATE_URL, GET_AFFILIATE_LEADERBOARD_URL, COUNTRIES_WITH_STATE


class AffiliateLeaderboardViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = ''
    serializer_class = []

    def list(self, request, *args, **kwargs):
        affiliate_name = request.query_params.get('affiliate_name')
        page = request.query_params.get('page', 1)
        affiliate_leaderboard_data = self.get_affiliate_leaderboard_data(affiliate_name, page)

        return Response(affiliate_leaderboard_data)

    def get_affiliate_leaderboard_data(self, affiliate_name, page):
        affiliate_id = self.get_affiliate_id(affiliate_name)
        if not affiliate_id:
            return []

        parameters = {
            "affiliate": affiliate_id,
            "division": 1,
            "scaled": 0,
            "page": page
        }

        url = GET_AFFILIATE_URL.format(datetime.utcnow().year)
        r = requests.get(url=url, params=parameters)

        if r.status_code != 200:
            raise Exception("failed to find gym leaderboard data")

        affiliate_leaderboard_data = r.json()

        return affiliate_leaderboard_data

    def get_affiliate_id(self, affiliate_name):
        parameters = {
            "term": affiliate_name,
        }

        url = GET_AFFILIATE_LEADERBOARD_URL.format(datetime.utcnow().year)
        r = requests.get(url=url, params=parameters)

        if r.status_code != 200:
            raise Exception("failed to locate gym")

        data = r.json()
        if len(data) == 0:
            return None
        affiliate_id = data[0].get('id')

        return affiliate_id
