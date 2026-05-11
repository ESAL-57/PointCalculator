import json

import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .calculator import calculate_player_positions, calculate_team, options_payload
from .riot import RiotApiError, lookup_player
from .scraper import crawl_sources, summarize_combined_ranks


def status(_request):
    return JsonResponse({"message": "Django API 연결 성공"})


def options(_request):
    return JsonResponse(options_payload())


@csrf_exempt
def calculate(request):
    if request.method != "POST":
        return JsonResponse({"message": "POST 요청만 지원합니다."}, status=405)

    try:
        payload = json.loads(request.body or "{}")
        result = calculate_team(payload.get("players", []))
    except ValueError as error:
        return JsonResponse({"message": str(error)}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({"message": "요청 형식이 올바르지 않습니다."}, status=400)

    return JsonResponse(result)


@csrf_exempt
def calculate_player(request):
    if request.method != "POST":
        return JsonResponse({"message": "POST 요청만 지원합니다."}, status=405)

    try:
        payload = json.loads(request.body or "{}")
        result = calculate_player_positions(payload.get("player", {}))
    except ValueError as error:
        return JsonResponse({"message": str(error)}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({"message": "요청 형식이 올바르지 않습니다."}, status=400)

    return JsonResponse(result)


def riot_player(request):
    game_name = request.GET.get("gameName", "").strip()
    tag_line = request.GET.get("tagLine", "").strip()

    if not game_name or not tag_line:
        return JsonResponse({"message": "닉네임과 태그를 입력해주세요."}, status=400)

    try:
        return JsonResponse(lookup_player(game_name, tag_line))
    except RiotApiError as error:
        return JsonResponse({"message": str(error)}, status=502)


def crawl_player(request):
    game_name = request.GET.get("gameName", "").strip()
    tag_line = request.GET.get("tagLine", "").strip()

    if not game_name or not tag_line:
        return JsonResponse({"message": "닉네임과 태그를 입력해주세요."}, status=400)

    riot = None
    riot_message = ""
    try:
        riot = lookup_player(game_name, tag_line)
    except RiotApiError as error:
        if "찾을 수 없습니다" in str(error):
            return JsonResponse(
                {"message": "존재하지 않는 닉네임 또는 태그입니다. 입력값을 다시 확인해주세요."},
                status=404,
            )
        riot_message = str(error)

    sources = crawl_sources(game_name, tag_line)

    return JsonResponse(
        {
            "riot": riot,
            "riotMessage": riot_message,
            "sources": sources,
            "summary": summarize_combined_ranks(sources, riot),
        }
    )


def riot_example(_request):
    if not settings.RIOT_API_KEY:
        return JsonResponse(
            {"message": "RIOT_API_KEY가 아직 설정되지 않았습니다."},
            status=503,
        )

    return JsonResponse(
        {
            "message": "Riot API 키가 설정되어 있습니다.",
            "region": settings.RIOT_REGION,
            "platform": settings.RIOT_PLATFORM,
        }
    )
