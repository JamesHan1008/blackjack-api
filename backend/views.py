from rest_framework import generics, views, response

from .models import Dealer
from .serializers import DealerSerializer
from .game_controller import *


class DealerListView(generics.ListCreateAPIView):
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer


class DealerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer


class DealerUpdateView(generics.UpdateAPIView):
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer


class StartGameView(views.APIView):

    def get(self, request, format=None):
        resp = start_game(
            dealer_id=request.query_params["dealer_id"],
        )
        return response.Response(resp)


class StartRoundView(views.APIView):

    def post(self, request, format=None):
        resp = start_round(
            state=request.data["state"],
            bet_amount=request.data["bet_amount"],
        )
        return response.Response(resp)


class PlayerHitView(views.APIView):

    def post(self, request, format=None):
        resp = player_hit(
            state=request.data["state"],
        )
        return response.Response(resp)


class PlayerStandView(views.APIView):

    def post(self, request, format=None):
        resp = player_stand(
            state=request.data["state"],
        )
        return response.Response(resp)


class PlayerDoubleView(views.APIView):

    def post(self, request, format=None):
        resp = player_double(
            state=request.data["state"],
        )
        return response.Response(resp)


class PlayerSplitView(views.APIView):

    def post(self, request, format=None):
        resp = player_split(
            state=request.data["state"],
        )
        return response.Response(resp)


class PlayerSurrenderView(views.APIView):

    def post(self, request, format=None):
        resp = player_surrender(
            state=request.data["state"],
        )
        return response.Response(resp)


class PlayerBuyInsuranceView(views.APIView):

    def post(self, request, format=None):
        resp = player_buy_insurance(
            state=request.data["state"],
        )
        return response.Response(resp)


class PlayerNoInsuranceView(views.APIView):

    def post(self, request, format=None):
        resp = player_no_insurance(
            state=request.data["state"],
        )
        return response.Response(resp)
