import os
import shutil

from rest_framework import viewsets, mixins
import requests

from app.constants import GET_GYM_ID_SEARCH_URL, GET_DETAILS_API_KEY, GET_GYM_DETAILS_SEARCH_URL, \
    GET_GYM_PHOTO_SEARCH_URL
from core.gym.model import Gym
from core.gym_details.model import GymDetails
from rest_framework.response import Response


class GymDetailsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = GymDetails.objects.all()
    serializer_class = []

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
            "fields": "international_phone_number,rating,review,photos,opening_hours",
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


