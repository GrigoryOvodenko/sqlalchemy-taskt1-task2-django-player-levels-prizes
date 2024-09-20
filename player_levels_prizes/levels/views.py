
import csv
import json

from django.http import HttpResponse, JsonResponse
from .models import PlayerLevel, LevelPrize,Prize
from django.views.decorators.csrf import csrf_exempt

from django.utils import timezone
import logging
logger = logging.getLogger(__name__)

@csrf_exempt
def award_prize(request):
    logger.info("Received request: %s", request)
    if request.method == "POST":
        data = json.loads(request.body)
        logger.info("Data: %s", data)
        player_level_id = data.get('player_level_id')
        prize_id = data.get('prize_id')
        try:
            player_level = PlayerLevel.objects.get(id=player_level_id)
        except PlayerLevel.DoesNotExist:
            return JsonResponse({'error': 'PlayerLevel not found'}, status=404)
        try:
            prize = Prize.objects.get(id=prize_id)
        except Prize.DoesNotExist:
            return JsonResponse({'error': 'Prize not found'}, status=404)

        if player_level.is_completed:
            LevelPrize.objects.create(
                level=player_level.level,
                prize=prize,
                received=timezone.now()
            )
            return JsonResponse({'status': 'Prize awarded successfully'})

        else:
            return JsonResponse({'error': 'Level not completed'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)



def export_player_levels_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="player_levels.csv"'

    writer = csv.writer(response)
    writer.writerow(['Player ID', 'Level Title', 'Is Completed', 'Prize Title'])

    player_levels = PlayerLevel.objects.select_related('player', 'level').prefetch_related('level__levelprize_set')

    for player_level in player_levels:
        prize_title = player_level.level.levelprize_set.first().prize.title if player_level.level.levelprize_set.exists() else 'No Prize'
        writer.writerow([
            player_level.player.player_id,
            player_level.level.title,
            player_level.is_completed,
            prize_title
        ])

    return response