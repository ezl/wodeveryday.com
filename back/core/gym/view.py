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
    def listSearchedLocation(self, request, *args):

        queryset = self.get_queryset()
        page_size=6
        page = request.query_params.get('page', 1)
        offset = (int(page) - 1) * page_size
        limit_plus_offset = offset + page_size

        search_text = request.query_params.get('search_text', "")
        # if there's no value, python will return None, which will break. give it a default *string* value

        search_text = [token for token in search_text.split(" ") if token]
        # wrapping it in a list comprehension that tests for falsiness will remove empty tokens.
        # as an example of why this is good, try "    foo     bar baz   ".split(" ")

        search_vectors = SearchVector('name') + SearchVector('continent') + SearchVector('country') + SearchVector('full_state') + SearchVector('city')
        # just a recommendation here, but most established dev teams will want to follow some sort
        # of maximum line length convention. I recommend checking out PEP8, the python style guide

        # tokenize search text and create search query
        search_queries = []
        for token in search_text:
            search_queries.append(Q(search__icontains=token))

        search_queries = reduce(operator.and_, search_queries)

        search_results = queryset.annotate(search=search_vectors).filter(search_queries).values('name', 'continent', 'country', 'full_state', 'city', 'name_slug')

        total = search_results.count()

        search_results = search_results[offset:limit_plus_offset]

        assembled_search_results = self.assembleSearchResults(search_results, search_text)
        # 1. if we add the search_text tokens here, we can use it to filter results in assembleSearchResults
        #
        # 2. also a note here -- generally the python style recommendation for methods is
        # to use assemble_search_results (underscore separated names) for functions
        # javascript tends to use lowerCaseStartCamelCased
        # python uses CapitalLetterStartCamelCasing for class names
        # these are just *conventions* and while the interpreter does not *require*
        # them, they are broadly accepted and generally a mark of someone who is experienced
        # in python. I think most developers would consider this a sign of whether or not
        # you have worked in a team that follows best practices. (Again, not a criticism,
        # just so you know for the next time you work with a team)

        total_pages = 0
        if total > 0:
            total_pages = math.ceil(total / page_size)

        response = {
            "meta": {
                "total_pages": total_pages
            },
            "data": assembled_search_results
        }

        return Response(response)

    def get_location_path(self, result, location_type):
        # first check if it's a gym. if so, kick it out and don't do
        # any of the geography stuff
        if location_type == "gym":
            location_path = "gym/" + result['name_slug']
            return location_path

        continent = result['continent']
        country = result['country']
        city = result['city']

        # BTW -- this is a crazy way to build the url -- i do NOT recommend it,
        # but I'm doing it this way because it is a similar way the original one is
        # built and I'm trying to not change the logic, just encapsulate it in
        # one place. Ultimately, I think using a urlresolver is the path, but
        # this way it can be just replaced more easily

        # basically I am using the same sequential build logic, then just kicking
        # out the function as soon as I hit the right level of depth

        # continent
        location_path = "find/" + continent.lower().replace(" ", "-")
        if location_type == "continent":
            return location_path

        # country
        location_path = location_path + "/" + country.lower().replace(" ", "-")
        if location_type == "country":
            return location_path

        # state
        location_path = location_path + "/" + state.lower().replace(" ", "-")
        if location_type == "state":
            return location_path

        # city
        location_path = location_path + "/" + city.lower().replace(" ", "-")
        if location_type == "city":
            return location_path

        # should never hit this
        raise Exception, "wtf, location type didn't match"

    def addToList(self, item_list, location_name, location_path, location_type):
        item = {
            "location_name": location_name,
            "location_path": location_path
            "location_type": location_type
        }
        if item not in item_list:
            item_list.append(item)
        return item_list

    def assembleSearchResults(self, search_results, search_text):
        continent_list = []
        country_list = []
        state_list = []
        city_list = []
        gym_list = []

        for result in search_results:
            continent = result['continent']
            country = result['country']
            city = result['city']

            # now that we have search text in here, let's use that as a filter
            # to decide whether to add this to the list

            if any([token in continent] for token in search_text]):
                location_type = 'continent'
                location_path = get_location_path(result, location_type)
                continent_list = self.addToList(continent_list, continent, location_path, location_type)


            if any([token in country] for token in search_text]):
                location_type = 'country'
                location_path = get_location_path(result, location_type)
                country_list = self.addToList(country_list, country + ", " + continent, location_path, location_type)

            if country in COUNTRIES_WITH_STATE:
                state = result['full_state']
                # there's definitely other ways to do this, but I'm trying to write as minimally invasive
                # code as possible
                if any([token in state] for token in search_text]):
                    location_type = 'state'
                    location_path = get_location_path(result, location_type)
                    state_list = self.addToList(state_list, state + ", " + country, location_path, location_type)

            # originally this was defaulting to this, but now explicitly checking before we add to the city list
            # ONLY if the city string matches a search token
            if any([token in city] for token in search_text]):
                location_type = 'city'
                location_path = get_location_path(result, location_type)
                # :sob: refactor
                city_list = self.addToList(city_list, city + ", " + state, location_path, location_type)

            name = result['name'] # really I'd put this up top, but just keeping similar logic structure
                                  # to what was originally written
            if any([token in name] for token in search_text]):
                location_type = 'gym'
                location_path = get_location_path(result, location_type)
                gym_list = self.addToList(gym_list, result['name'] + ", " + city, location_path, location_type)

        assembled_search_results = list(itertools.chain.from_iterable([
            continent_list,
            country_list,
            state_list,
            city_list,
            gym_list
        ]))
        # BTW -- what's going on here? aren't these already lists?
        # if so, list1 + list2 + list3 should do this.
        # for example:
        # list1 = [1,2,3]
        # list2 = [4,5,]
        # list3 = []
        # list4 = [6,7,8,9,10]
        # combined = list1 + list2 + list3 + list4
        # combined will be [1,2,3,4,5,6,7,8,9,10]
        # (i could be misunderstanding your purpose though, so disregard if i've misunderstood)

        return assembled_search_results

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
