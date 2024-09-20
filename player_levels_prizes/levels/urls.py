from django.urls import path
from .views import award_prize, export_player_levels_to_csv

urlpatterns = [
    path('award_prize/', award_prize, name='award_prize'),
    path('export-csv/', export_player_levels_to_csv, name='export_csv'),
]