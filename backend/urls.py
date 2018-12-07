from django.urls import path

from . import views


urlpatterns = [
    path("dealers/", views.DealerListView.as_view()),
    path("dealers/<int:pk>/", views.DealerDetailView.as_view()),
    path("dealers/update/<int:pk>/", views.DealerUpdateView.as_view()),

    path("game/start_game/", views.StartGameView.as_view()),
    path("game/start_round/", views.StartRoundView.as_view()),
    path("game/player_hit/", views.PlayerHitView.as_view()),
    path("game/player_stand/", views.PlayerStandView.as_view()),
    path("game/player_double/", views.PlayerDoubleView.as_view()),
    path("game/player_split/", views.PlayerSplitView.as_view()),
    path("game/player_surrender/", views.PlayerSurrenderView.as_view()),
    path("game/player_buy_insurance/", views.PlayerBuyInsuranceView.as_view()),
    path("game/player_no_insurance/", views.PlayerNoInsuranceView.as_view()),
]
