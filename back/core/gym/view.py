import operator
from functools import reduce
from itertools import chain

from django.db.models import Q
from rest_framework import viewsets, mixins, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from core.gym.model import Gym
from core.gym.serializer import GymSerializer
from django_filters.rest_framework import DjangoFilterBackend
from app.constants import GET_GYM_URL, GET_GYM_LEADERBOARD_URL, COUNTRIES_WITH_STATE


class GymViewSet(mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):

    queryset = Gym.objects.all()
    serializer_class = GymSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name']
    filterset_fields = {
            'country': ['iexact'],
            'full_state': ['iexact'],
            'city': ['iexact'],
            'name': ['iexact'],
            'name_slug': ['iexact']
        }

    @action(detail=False, methods=['get'], url_path='search_locations')
    def listSearchedLocation(self, request, *args):

        queryset = self.get_queryset()
        search_text = request.query_params.get('search_text')
        search_text = search_text.split(" ")

        # tokenize search text and create search query
        search_query = []
        for token in search_text:
            additional_search_query = [Q(city__icontains=token), Q(full_state__icontains=token), Q(country__icontains=token), Q(continent__icontains=token)]
            additional_search_query = reduce(operator.or_, additional_search_query)
            search_query.append(additional_search_query)

        search_query = reduce(operator.and_, search_query)

        # fetch segments of search
        cities_with_states_list = queryset.exclude(full_state__isnull=False).filter(search_query) \
            .values_list('city', 'country').distinct()[:5]

        cities_without_states_list = queryset.exclude(full_state__isnull=True).filter(search_query) \
            .values_list('city', 'full_state').distinct()[:5]

        continents_and_countries = queryset.filter(search_query) \
            .values_list('country', 'continent').distinct()[:5]

        countries_and_states = queryset.filter(search_query).exclude(full_state__isnull=True) \
                                                   .values_list('full_state', 'country').distinct()[:5]

        # combine search segments
        response_body = chain(cities_without_states_list, cities_with_states_list, countries_and_states, continents_and_countries)
        list_of_searched_locations = []
        for location_tuple in response_body:
            list_of_searched_locations.append(", ".join(location_tuple))

        return Response(list_of_searched_locations)

    @action(detail=False, methods=['get'], url_path='slugs')
    def listGymSlugs(self, request, *args):

        queryset = self.get_queryset()
        gym_slugs_list = queryset.values_list('name_slug', flat=True)

        return Response(gym_slugs_list)

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
            gyms_by_city_or_state_dictionary[key] = queryset.filter(Q(city__iexact=key), query) \
                .values_list('name', 'name_slug') \
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
