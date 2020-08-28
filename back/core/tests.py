from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.gym.models import Gym


class GymViewTestCases(APITestCase):
    BASE_URL = reverse("gym-list")
    CONTINENTS_URL = BASE_URL + "continents/"
    COUNTRIES_URL = BASE_URL + "countries/"
    STATES_URL = BASE_URL + "states/"
    GYMS_URL = BASE_URL + "gyms/"
    TEST_GYM_OBJECT_WITH_STATE = {
        'website': 'http://somegym.com/',
        'photo': 'http://somegymicon.com/image.png',
        'ready_to_link': '1',
        'ordernum': '2121',
        'lat': '50.82342',
        'lon': '-0.12341234',
        'city': 'Ontario City',
        'name_search': 'somegym',
        'photo_version': '0',
        'zip': '11111',
        'country_short_code': 'SW',
        'bad_standing': '0',
        'effective_date': '2007-12-07T08:00:00Z',
        'status': '1',
        'address': '632 somewhere street',
        'active': '1',
        'state_code': None,
        'show_on_map': '1',
        'kids': '0',
        'name': 'somegym',
        'country': 'Canada',
        'org_type': 'Commercial',
        'aid': '469',
        'full_state': "Ontario",
        'continent': 'North America'
    }
    TEST_GYM_OBJECT_WITHOUT_STATE = {
        'website': 'http://somegym.com/',
        'photo': 'http://somegymicon.com/image.png',
        'ready_to_link': '1',
        'ordernum': '2121',
        'lat': '50.82342',
        'lon': '-0.12341234',
        'city': 'Bulgaria City',
        'name_search': 'somegym',
        'photo_version': '0',
        'zip': '11111',
        'country_short_code': 'SW',
        'bad_standing': '0',
        'effective_date': '2007-12-07T08:00:00Z',
        'status': '1',
        'address': '632 somewhere street',
        'active': '1',
        'state_code': None,
        'show_on_map': '1',
        'kids': '0',
        'name': 'somegym',
        'country': 'Bulgaria',
        'org_type': 'Commercial',
        'aid': '469',
        'full_state': None,
        'continent': 'Europe'
    }

    def setUp(self):
        self.maxDiff = None
        Gym.objects.create(**self.TEST_GYM_OBJECT_WITH_STATE)
        Gym.objects.create(**self.TEST_GYM_OBJECT_WITHOUT_STATE)

    def test_list_continents_and_countries(self):
        response = self.client.get(self.CONTINENTS_URL)

        expected_response_body = {
            'Africa': [],
            'Asia': [],
            'Europe': [
                self.TEST_GYM_OBJECT_WITHOUT_STATE['country']
            ],
            'North America': [
                self.TEST_GYM_OBJECT_WITH_STATE['country']
            ],
            'South America': [],
            'Oceania': []
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response_body)

    def test_list_countries_and_states_by_continent(self):
        response = self.client.get(self.COUNTRIES_URL, {"continent": self.TEST_GYM_OBJECT_WITH_STATE['continent']})

        expected_response_body = {
            self.TEST_GYM_OBJECT_WITH_STATE['country']: [self.TEST_GYM_OBJECT_WITH_STATE['full_state']]}

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response_body)

    def test_list_countries_and_cities_by_continent(self):
        response = self.client.get(self.COUNTRIES_URL, {"continent": self.TEST_GYM_OBJECT_WITHOUT_STATE['continent']})

        expected_response_body = {
            self.TEST_GYM_OBJECT_WITHOUT_STATE['country']: [self.TEST_GYM_OBJECT_WITHOUT_STATE['city']]}

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response_body)

    def test_list_states_and_cities_by_country(self):
        response = self.client.get(self.STATES_URL, {"country": self.TEST_GYM_OBJECT_WITH_STATE['country']})

        expected_response_body = {
            self.TEST_GYM_OBJECT_WITH_STATE['full_state']: [self.TEST_GYM_OBJECT_WITH_STATE['city']]}

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response_body)

    def test_list_cities_and_gyms_by_state(self):
        response = self.client.get(self.GYMS_URL, {"state": self.TEST_GYM_OBJECT_WITH_STATE['full_state']})

        expected_response_body = {self.TEST_GYM_OBJECT_WITH_STATE['city']: [self.TEST_GYM_OBJECT_WITH_STATE['name']]}

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response_body)

    def test_list_gyms_by_city_and_country(self):
        response = self.client.get(self.BASE_URL, {"city__iexact": self.TEST_GYM_OBJECT_WITHOUT_STATE['city'],
                                                   "country__iexact": self.TEST_GYM_OBJECT_WITHOUT_STATE['country']})

        expected_result_object = self.TEST_GYM_OBJECT_WITHOUT_STATE
        expected_result_object['id'] = 2
        expected_response_body = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                expected_result_object
            ]
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response_body)

    def test_list_gyms_by_city_country_and_state(self):
        response = self.client.get(self.BASE_URL, {"city__iexact": self.TEST_GYM_OBJECT_WITH_STATE['city'],
                                                   "country__iexact": self.TEST_GYM_OBJECT_WITH_STATE['country'],
                                                   "state__iexact": self.TEST_GYM_OBJECT_WITH_STATE['full_state']})

        expected_result_object = self.TEST_GYM_OBJECT_WITH_STATE
        expected_result_object['id'] = 1
        expected_response_body = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                expected_result_object
            ]
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response_body)

    def test_list_gyms_by_city_and_name(self):
        response = self.client.get(self.BASE_URL, {"name__iexact": self.TEST_GYM_OBJECT_WITH_STATE['name'],
                                                   "city__iexact": self.TEST_GYM_OBJECT_WITH_STATE['city']})

        expected_result_object = self.TEST_GYM_OBJECT_WITH_STATE
        expected_result_object['id'] = 1
        expected_response_body = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                expected_result_object
            ]
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response_body)
