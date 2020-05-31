from django.db.models import Q
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from quickstart.affiliate.model import Affiliate
from quickstart.affiliate.serializer import AffiliateSerializer
from django_filters.rest_framework import DjangoFilterBackend
from app.constants import GET_AFFILIATE_URL, GET_AFFILIATE_LEADERBOARD_URL, COUNTRIES_WITH_STATE


class AffiliateViewSet(mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):

    queryset = Affiliate.objects.all()
    serializer_class = AffiliateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
            'country': ['iexact'],
            'full_state': ['iexact'],
            'city': ['iexact'],
            'name': ['iexact']
        }

    @action(detail=False, methods=['get'], url_path='continents')
    def listDistinctCountriesByContinent(self, request, *args):

        queryset = self.get_queryset()
        country_by_continent_dictionary = {
            "Africa": [],
            "Asia": [],
            "Europe": [],
            "North America": [],
            "South America": [],
            "Oceania": [],
        }
        for key, value in country_by_continent_dictionary.copy().items():
            country_by_continent_dictionary[key] = queryset.filter(continent__iexact=key)\
                                   .values_list('country', flat=True) \
                                   .order_by('country') \
                                   .distinct()

        return Response(country_by_continent_dictionary)

    @action(detail=False, methods=['get'], url_path='countries')
    def listDistinctCountriesAndTheirCitiesByContinent(self, request, *args):

        continent = request.query_params.get('continent', '')
        queryset = self.get_queryset()

        countries_list = queryset.filter(continent__iexact=continent) \
            .values_list('country', flat=True) \
            .order_by('country') \
            .distinct()

        countries_by_continent_dictionary = dict.fromkeys(countries_list, []).items()

        countries_by_continent_dictionary = self.build_countries_by_continent_dict(countries_by_continent_dictionary,
                                                                                   queryset)
        return Response(countries_by_continent_dictionary)

    @action(detail=False, methods=['get'], url_path='states')
    def listDistinctStatesAndTheirCitiesByCountry(self, request, *args):

        country = request.query_params.get('country', '')
        queryset = self.get_queryset()

        state_list = queryset.filter(country__iexact=country) \
            .values_list('full_state', flat=True) \
            .order_by('full_state') \
            .distinct()

        cities_by_state_dictionary = dict.fromkeys(state_list, [])

        for key, value in cities_by_state_dictionary.copy().items():
            cities_by_state_dictionary[key] = queryset.filter(full_state__iexact=key) \
                                                    .values_list('city', flat=True) \
                                                    .order_by('city') \
                                                    .distinct()

        return Response(cities_by_state_dictionary)

    @action(detail=False, methods=['get'], url_path='gyms')
    def listDistinctCitiesAndTheirGymsByCountryOrState(self, request, *args):

        country = request.query_params.get('country', '')
        if not country:
            state = request.query_params.get('state', '')
            query = Q(full_state__iexact=state)
        else:
            query = Q(country__iexact=country)
        queryset = self.get_queryset()

        city_or_state_list = queryset.filter(query) \
            .values_list('city', flat=True) \
            .order_by('city') \
            .distinct()

        gyms_by_city_or_state_dictionary = dict.fromkeys(city_or_state_list, [])

        for key, value in gyms_by_city_or_state_dictionary.copy().items():
            gyms_by_city_or_state_dictionary[key] = queryset.filter(city__iexact=key) \
                .values_list('name', flat=True) \
                .order_by('name') \
                .distinct()

        return Response(gyms_by_city_or_state_dictionary)

    @staticmethod
    def build_countries_by_continent_dict(original_dictionary, queryset):
        new_dictionary = {}
        for key, value in original_dictionary:
            if key in COUNTRIES_WITH_STATE:
                new_dictionary[key] = queryset.filter(country__iexact=key) \
                    .values_list('full_state', flat=True) \
                    .order_by('full_state') \
                    .distinct()
            else:
                new_dictionary[key] = queryset.filter(country__iexact=key) \
                    .values_list('city', flat=True) \
                    .order_by('city') \
                    .distinct()

        return new_dictionary
