import itertools
import math
import operator
from functools import reduce
from django.contrib.postgres.search import SearchVector
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
    def list_searched_locations(self, request, *args):

        queryset = self.get_queryset()
        page_size = 6
        page = request.query_params.get('page', 1)
        offset = (int(page) - 1) * page_size
        limit_plus_offset = offset + page_size

        search_text = request.query_params.get('search_text', None)
        if search_text is None or len(search_text) < 3:
            return self.list_searched_location_response(0, [])

        search_text = [token for token in search_text.split(" ") if token]
        search_vectors = SearchVector('name') + SearchVector('continent') + SearchVector('country') + SearchVector(
            'full_state') + SearchVector('city')

        search_queries = []
        for token in search_text:
            search_queries.append(Q(search__icontains=token))

        search_queries = reduce(operator.and_, search_queries)

        search_results = queryset.annotate(search=search_vectors).filter(search_queries).values('name', 'continent',
                                                                                                'country', 'full_state',
                                                                                                'city', 'name_slug')

        total = search_results.count()

        search_results = search_results[offset:limit_plus_offset]

        assembled_search_results = self.assemble_search_results(search_results, search_text)

        total_pages = 0
        if total > 0:
            total_pages = math.ceil(total / page_size)

        return self.list_searched_location_response(total_pages, assembled_search_results)

    @staticmethod
    def list_searched_location_response(total_pages, assembled_search_results):

        response = {
            "meta": {
                "total_pages": total_pages
            },
            "data": assembled_search_results
        }

        return Response(response)

    @staticmethod
    def add_to_list(search_text, item_list, location_path, location_name, location_type):
        item = {
            "location_name": f"{location_name} ({location_type})",
            "location_path": location_path.lower().replace(" ", "-")
        }
        if item not in item_list and any(token in location_name.lower() for token in search_text):
            item_list.append(item)
        return item_list

    def assemble_search_results(self, search_results, search_text):
        continent_list = []
        country_list = []
        state_list = []
        city_list = []
        gym_list = []

        for result in search_results:
            continent = result['continent']
            country = result['country']
            city = result['city']
            gym_name = result['name']
            gym_slug = result['name_slug']

            location_path = "find/" + continent
            continent_list = self.add_to_list(search_text, continent_list, location_path, location_name=continent,
                                              location_type='continent')

            location_path = location_path + "/" + country
            country_list = self.add_to_list(search_text, country_list, location_path,
                                            location_name=country + ", " + continent, location_type='country')

            if country in COUNTRIES_WITH_STATE:
                state = result['full_state']
                location_path = location_path + "/" + state
                state_list = self.add_to_list(search_text, state_list, location_path,
                                              location_name=state + ", " + country, location_type='state')

                location_path = location_path + "/" + city
                city_list = self.add_to_list(search_text, city_list, location_path, location_name=city + ", " + state,
                                             location_type='city')
            else:
                location_path = location_path + "/" + city
                city_list = self.add_to_list(search_text, city_list, location_path, location_name=city + ", " + country,
                                             location_type='city')

            gym_list = self.add_to_list(search_text, gym_list, location_path="gym/" + gym_slug,
                                        location_name=gym_name + ", " + city, location_type='gym')

        assembled_search_results = list(itertools.chain.from_iterable([
            continent_list,
            country_list,
            state_list,
            city_list,
            gym_list
        ]))

        return assembled_search_results

    @action(detail=False, methods=['get'], url_path='slugs')
    def list_gym_slugs(self, request, *args):

        queryset = self.get_queryset()
        gym_slugs_list = queryset.values_list('name_slug', flat=True)

        return Response(gym_slugs_list)

    @action(detail=False, methods=['get'], url_path='continents')
    def list_distinct_countries_by_continent(self, request, *args):

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
            country_by_continent_dictionary[key] = queryset.filter(continent__iexact=key) \
                .values_list('country', flat=True) \
                .order_by('country') \
                .distinct()

        return Response(country_by_continent_dictionary)

    @action(detail=False, methods=['get'], url_path='countries')
    def list_distinct_countries_and_their_cities_by_continent(self, request, *args):

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
    def list_distinct_states_and_their_cities_by_country(self, request, *args):

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
    def list_distinct_cities_and_their_gyms_by_country_or_state(self, request, *args):

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
