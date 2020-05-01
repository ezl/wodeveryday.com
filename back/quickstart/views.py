import requests
from django.db.models import Q
from rest_framework import viewsets, mixins, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from quickstart.models import Affiliate
from quickstart.serializers import AffiliateSerializer
from django_filters.rest_framework import DjangoFilterBackend


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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['country', 'full_state', 'city']

    @action(detail=False, methods=['get'], url_path='countries')
    def listDistinctCountries(self, request, *args):

        queryset = self.get_queryset()
        country_list = queryset.values_list('country', flat=True)\
                               .distinct()

        return Response({"countries": country_list})

    @action(detail=False, methods=['get'], url_path='states')
    def listDistinctStates(self, request, *args):

        country = request.query_params.get('country', '')
        queryset = self.get_queryset()
        state_list = queryset.filter(country=country)\
                             .values_list('full_state', flat=True)\
                             .distinct()

        if state_list is None:
            state_list = []

        return Response({"states": state_list})

    @action(detail=False, methods=['get'], url_path='cities')
    def listDistinctCities(self, request, *args):

        country = request.query_params.get('country', '')
        if not country:
            state = request.query_params.get('state', '')
            query = Q(full_state=state)
        else:
            query = Q(country=country)

        queryset = self.get_queryset()
        city_list = queryset.filter(query)\
                            .values_list('city', flat=True)\
                            .distinct()

        if city_list is None:
            city_list = []

        return Response({"cities": city_list})
