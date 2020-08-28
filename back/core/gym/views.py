from datetime import datetime
import itertools
import math
import operator
from functools import reduce

import requests
from django.contrib.postgres.search import SearchVector
from django.db.models import Q

from rest_framework import viewsets, mixins, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from core.gym.models import Gym, GymDetails, GymLeaderboard
from core.gym.serializer import GymSerializer
from app.constants import (
    GET_GYM_URL,
    GET_GYM_ID_SEARCH_URL,
    GET_DETAILS_API_KEY,
    GET_GYM_DETAILS_SEARCH_URL,
    GET_GYM_PHOTO_SEARCH_URL,
    GET_GYM_LEADERBOARD_URL,
    COUNTRIES_WITH_STATE
)


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

        # fetch and calculate pagination
        page_size = 100
        page = request.query_params.get('page', 1)
        offset = (int(page) - 1) * page_size
        limit_plus_offset = offset + page_size

        # fetch, verify, and tokenize search_text
        search_text = request.query_params.get('search_text', None)
        if search_text is None or len(search_text) < 3:
            return self.list_searched_location_response(0, [])
        search_text = [token for token in search_text.split(" ") if token]

        # fetch, count, paginate, and format search results
        search_results_dictionary = {
            'continent': ['continent'],
            'country': ['country', 'continent'],
            'full_state': ['full_state', 'country', 'continent'],
            'city': ['city', 'full_state', 'country', 'continent'],
            'name': ['name', 'city', 'name_slug']
        }
        search_results = []
        for key, value, in search_results_dictionary.items():
            search_results.append(
                queryset.filter(self.generate_search_query(search_text, value[0])).values(*value).distinct()
            )
        search_results = list(itertools.chain(*search_results))
        total = len(search_results)
        search_results = search_results[offset:limit_plus_offset]
        assembled_search_results = self.assemble_search_results(search_results)

        # build and return response
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

    def assemble_search_results(self, search_results):
        assembled_search_results = []
        for result in search_results:
            location_path, location_name, location_type = self.get_location_info(result)
            if location_path is None and location_name is None and location_type is None:
                continue
            assembled_search_results.append(self.add_to_list(location_path, location_name, location_type))

        return assembled_search_results

    @staticmethod
    def get_location_info(location_object):
        lo = location_object  # slim down object name to highlight field names retrieved from it
        if lo.get('name', False):
            return (f"gym/{lo['name_slug']}",
                    f"{lo['name']}, {lo['city']}",
                    'gym')

        if lo.get('city', False):
            if lo['country'] in COUNTRIES_WITH_STATE:
                return (f"find/{lo['continent']}/{lo['country']}/{lo['full_state']}/{lo['city']}",
                        f"{lo['city']}, {lo['full_state']}",
                        'city')
            else:
                return (f"find/{lo['continent']}/{lo['country']}/{lo['city']}",
                        f"{lo['city']}, {lo['country']}",
                        'city')

        if lo.get('full_state', False):
            return (f"find/{lo['continent']}/{lo['country']}/{lo['full_state']}",
                    f"{lo['full_state']}, {lo['country']}",
                    'state')

        if lo.get('country', False):
            return (f"find/{lo['continent']}/{lo['country']}",
                    f"{lo['country']}, {lo['continent']}",
                    'country')

        if lo.get('continent', False):
            return (f"find/{lo['continent']}",
                    lo['continent'],
                    'continent')

        return (None, None, None)

    @staticmethod
    def add_to_list(location_path, location_name, location_type):
        item = {
            "location_name": location_name,
            "location_path": location_path.lower().replace(" ", "-"),
            "location_type": location_type
        }
        return item

    @staticmethod
    def generate_search_query(search_tokens, search_field):
        search_queries = []
        for token in search_tokens:
            kwargs = {f"{search_field}__icontains": token}
            search_queries.append(Q(**kwargs))

        search_queries = reduce(operator.and_, search_queries)
        return search_queries

    @action(detail=False, methods=['get'], url_path='slugs')
    def list_gym_slugs(self, request, *args):

        queryset = self.get_queryset()
        gym_slugs_list = queryset.values_list('name_slug', flat=True)

        return Response(gym_slugs_list)

    @action(detail=False, methods=['get'], url_path='continents')
    def list_distinct_countries_by_continent(self, request, *args):

        queryset = self.get_queryset()
        country_by_continent_dictionary = {
            "Oceania": [],
            "South America": [],
            "North America": [],
            "Europe": [],
            "Asia": [],
            "Africa": [],
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
            .order_by('-country') \
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
            .order_by('-full_state') \
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
            .order_by('-city') \
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


class GymDetailsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = GymDetails.objects.all()
    serializer_class = []

    @action(detail=False, methods=['put'], url_path='update_photos')
    def update_photos(self, request, *args):
        gym_details_api_id = request.data.get('place_id')
        photos = request.data.get('photos')

        gym_details_object = GymDetails.objects.get(gym_details_api_id=gym_details_api_id)
        gym_details_object.data[0]['photos'] = photos
        gym_details_object.save()

        return Response(gym_details_object.data)

    def list(self, request, *args, **kwargs):
        gym_search_query = request.query_params.get('gym_search_query')
        gym_id = request.query_params.get('gym_id')

        gym_details = self.process_gym_details_request(gym_search_query, gym_id)

        return Response(gym_details)

    def process_gym_details_request(self, gym_search_query, gym_id):
        gym_object = Gym.objects.get(id=gym_id)
        gym_has_details = hasattr(gym_object, 'gymdetails')

        if gym_has_details:
            gym_details = gym_object.gymdetails.data
            gym_details[0]["place_id"] = gym_object.gymdetails.gym_details_api_id
            return gym_details
        else:
            gym_details_api_id = self.get_gym_details_api_id(gym_search_query)

        gym_details = self.get_gym_details(gym_details_api_id)
        gym_details["place_id"] = gym_details_api_id

        self.create_details_data(gym_object, gym_details, gym_details_api_id)

        # gym_details is an dictionary in a list when returned from the database.
        # gym_details is an dictionary when it is fetched from the api.
        # To maintain a contract with the frontend, both should be returned as an dictionary in a list
        return [gym_details]

    def create_details_data(self, gym_object, gym_details, gym_details_api_id):
        gym_details_object = GymDetails(gym=gym_object, gym_details_api_id=gym_details_api_id, data=[gym_details])
        gym_details_object.save()

    def get_gym_details(self, gym_details_api_id):
        parameters = {
            "place_id": gym_details_api_id,
            "fields": "international_phone_number,rating,review,opening_hours",
            "key": GET_DETAILS_API_KEY
        }

        url = GET_GYM_DETAILS_SEARCH_URL
        r = requests.get(url=url, params=parameters)

        if r.status_code != 200:
            raise Exception("failed to locate gym")

        data = r.json()
        gym_details = data.get("result")

        return gym_details

    def get_gym_details_api_id(self, gym_search_query):
        parameters = {
            "input": gym_search_query,
            "inputtype": "textquery",
            "fields": "place_id",
            "key": GET_DETAILS_API_KEY
        }

        url = GET_GYM_ID_SEARCH_URL
        r = requests.get(url=url, params=parameters)

        if r.status_code != 200:
            raise Exception("failed to locate gym")

        data = r.json()
        if len(data) == 0 or len(data.get("candidates")) == 0:
            raise Exception("failed to locate gym")

        gym_details_api_id = data.get("candidates")[0].get("place_id")

        return gym_details_api_id


class GymLeaderboardViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = GymLeaderboard.objects.all()
    serializer_class = []

    def list(self, request, *args, **kwargs):
        gym_name = request.query_params.get('gym_name')
        gym_id = request.query_params.get('gym_id')
        page = request.query_params.get('page', 1)

        gym_leaderboard = self.process_gym_leaderboard_request(gym_name, gym_id, page)

        return Response(gym_leaderboard)

    def process_gym_leaderboard_request(self, gym_name, gym_id, page):

        gym_object = Gym.objects.get(id=gym_id)
        gym_has_leaderboard = hasattr(gym_object, 'gymleaderboard')

        if gym_has_leaderboard:
            try:
                gym_leaderboard_data = gym_object.gymleaderboard.data
                return gym_leaderboard_data
            except Exception as e:
                leaderboard_api_id = gym_object.gymleaderboard.leaderboard_api_id
        else:
            leaderboard_api_id = self.get_leaderboard_api_id(gym_name)

        gym_leaderboard_data = self.get_gym_leaderboard_data(leaderboard_api_id, page)

        self.create_or_update_leaderboard_data(gym_has_leaderboard, gym_object, gym_leaderboard_data,
                                               leaderboard_api_id)

        # gym_leaderboard_data is an dictionary in a list when returned from the database.
        # gym_leaderboard_data is an dictionary when it is fetched from the api.
        # To maintain a contract with the frontend, both should be returned as an dictionary in a list
        return [gym_leaderboard_data]

    def create_or_update_leaderboard_data(self, gym_has_leaderboard, gym_object, gym_leaderboard_data,
                                          leaderboard_api_id):
        if gym_has_leaderboard:
            gym_leaderboard_object = GymLeaderboard.objects.get(leaderboard_api_id=leaderboard_api_id)
            gym_leaderboard_object.data.append(gym_leaderboard_data)
            gym_leaderboard_object.save()
        else:
            gym_leaderboard_object = GymLeaderboard(gym=gym_object, leaderboard_api_id=leaderboard_api_id,
                                                    data=[gym_leaderboard_data])
            gym_leaderboard_object.save()

    def get_gym_leaderboard_data(self, leaderboard_api_id, page):

        parameters = {
            "affiliate": leaderboard_api_id,
            "division": 1,
            "scaled": 0,
            "page": page
        }

        url = GET_GYM_URL.format(datetime.utcnow().year)
        r = requests.get(url=url, params=parameters)

        if r.status_code != 200:
            raise Exception("failed to find gym leaderboard data")

        gym_leaderboard_data = r.json()

        return gym_leaderboard_data

    def get_leaderboard_api_id(self, gym_name):
        parameters = {
            "term": gym_name,
        }

        url = GET_GYM_LEADERBOARD_URL.format(datetime.utcnow().year)
        r = requests.get(url=url, params=parameters)

        if r.status_code != 200:
            raise Exception("failed to locate gym")

        data = r.json()
        if len(data) == 0:
            raise Exception("failed to locate gym")

        leaderboard_api_id = data[0].get('id')

        return leaderboard_api_id
