from urllib.parse import quote

import requests
from django.conf import settings


class RiotApiError(Exception):
    pass


def riot_get(url):
    if not settings.RIOT_API_KEY:
        raise RiotApiError("RIOT_API_KEY가 설정되지 않았습니다.")

    response = requests.get(
        url,
        headers={"X-Riot-Token": settings.RIOT_API_KEY},
        timeout=10,
    )

    if response.status_code == 404:
        raise RiotApiError("Riot 계정을 찾을 수 없습니다.")
    if response.status_code == 403:
        raise RiotApiError("Riot API 키가 만료되었거나 권한이 없습니다.")
    if response.status_code == 429:
        raise RiotApiError("Riot API 요청 제한에 걸렸습니다. 잠시 후 다시 시도해주세요.")
    if not response.ok:
        raise RiotApiError(f"Riot API 요청 실패: {response.status_code}")

    return response.json()


def lookup_player(game_name, tag_line):
    region = settings.RIOT_REGION
    platform = settings.RIOT_PLATFORM
    encoded_name = quote(game_name)
    encoded_tag = quote(tag_line)

    account = riot_get(
        f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/"
        f"{encoded_name}/{encoded_tag}"
    )
    summoner = riot_get(
        f"https://{platform}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/"
        f"{account['puuid']}"
    )
    leagues = riot_get(
        f"https://{platform}.api.riotgames.com/lol/league/v4/entries/by-puuid/"
        f"{account['puuid']}"
    )

    solo_rank = next(
        (entry for entry in leagues if entry.get("queueType") == "RANKED_SOLO_5x5"),
        None,
    )
    flex_rank = next(
        (entry for entry in leagues if entry.get("queueType") == "RANKED_FLEX_SR"),
        None,
    )

    return {
        "account": {
            "gameName": account.get("gameName", game_name),
            "tagLine": account.get("tagLine", tag_line),
            "puuid": account.get("puuid"),
        },
        "summoner": {
            "id": summoner.get("id"),
            "puuid": summoner.get("puuid"),
            "summonerLevel": summoner.get("summonerLevel"),
            "profileIconId": summoner.get("profileIconId"),
        },
        "leagues": leagues,
        "soloRank": solo_rank,
        "flexRank": flex_rank,
    }
