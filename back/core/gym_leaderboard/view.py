from datetime import datetime
import requests
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from app.constants import GET_GYM_URL, GET_GYM_LEADERBOARD_URL, COUNTRIES_WITH_STATE
from core.gym_leaderboard.model import GymLeaderboard
from core.gym.model import Gym


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

    def create_or_update_leaderboard_data(self, gym_has_leaderboard, gym_object, gym_leaderboard_data, leaderboard_api_id):
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
