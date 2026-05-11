import re
import json
from urllib.parse import quote

import requests


class ScrapeError(Exception):
    pass


ROMAN_DIVISIONS = {
    "I": "1",
    "II": "2",
    "III": "3",
    "IV": "4",
    "V": "5",
}


def fetch_page(url):
    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 PointCalculator test crawler",
            "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
        },
        timeout=12,
    )
    if not response.ok:
        raise ScrapeError(f"{response.status_code} 응답")
    return response.text


def extract_tier_mentions(html):
    normalized_html = html.replace("\\", "")
    patterns = [
        r"마/그/챌\s*\d+\s*(?:~\s*\d+|이상)?",
        r"(?:다이아|에메랄드|플래티넘|골드|실버|브론즈|아이언)\s*[1-4]",
        r"(?:MASTER|GRANDMASTER|CHALLENGER|DIAMOND|EMERALD|PLATINUM|GOLD|SILVER|BRONZE|IRON)\s*(?:I{1,3}|IV|[1-4])?",
    ]
    mentions = []
    for pattern in patterns:
        mentions.extend(re.findall(pattern, normalized_html, flags=re.IGNORECASE))

    cleaned = []
    for mention in mentions:
        value = re.sub(r"\s+", "", mention.strip())
        if value and value not in cleaned:
            cleaned.append(value)
    return cleaned[:20]


def extract_opgg_season_ranks(html):
    normalized_html = html.replace('\\"', '"').replace("\\n", "")
    match = re.search(
        r'"data":(\[{"season":"S2025.*?}\]),"queueType":"SOLORANKED"',
        normalized_html,
    )
    if not match:
        return []

    try:
        season_data = json.loads(match.group(1))
    except json.JSONDecodeError:
        return []

    ranks = []
    for item in season_data:
        season = item.get("season", "").strip()

        rank_entries = item.get("rank_entries") or {}
        high_rank = rank_entries.get("high_rank_info") or {}
        final_rank = rank_entries.get("rank_info") or {}
        ranks.append(
            {
                "season": season,
                "highRank": {
                    "tier": high_rank.get("tier") or "",
                    "lp": high_rank.get("lp"),
                },
                "rank": {
                    "tier": final_rank.get("tier") or "",
                    "lp": final_rank.get("lp"),
                },
            }
        )

    return ranks


def extract_opgg_current_highest_rank(html):
    normalized_html = html.replace('\\"', '"').replace("\\n", "")
    label_index = normalized_html.find('"children":"최고 티어"')
    if label_index == -1:
        return None

    before_label = normalized_html[max(0, label_index - 1600) : label_index]
    matches = re.findall(
        r'"children":"([^"]+)"\}\],\["\$","span",null,\{"className":"text-xs text-gray-500","children":\["([^"]+)"," LP"\]',
        before_label,
    )
    if not matches:
        return None

    tier, lp = matches[-1]
    return {
        "tier": tier,
        "lp": lp.replace(",", ""),
    }


def normalize_scraped_tier(tier, division):
    tier = tier.lower()
    if tier in ["master", "grandmaster", "challenger"]:
        return tier
    return f"{tier} {ROMAN_DIVISIONS.get(division, division)}"


def extract_fow_solo_ranks(html):
    ranks = []
    seen = set()

    for block in re.split(r"<HR>", html, flags=re.IGNORECASE):
        if "솔로랭크" not in block:
            continue

        season_match = re.search(
            r"솔로랭크\s+S(?P<season>\d+(?:\s*-\s*\d+)?)|시즌\s*(?P<old_season>\d+)\s*\((?P<old_split>\d+)\).*?솔로랭크",
            block,
            flags=re.IGNORECASE | re.DOTALL,
        )
        high_match = re.search(
            r"최고\s*기록\s*:\s*"
            r"(?P<tier>IRON|BRONZE|SILVER|GOLD|PLATINUM|EMERALD|DIAMOND|MASTER|GRANDMASTER|CHALLENGER)"
            r"\s+(?P<division>I{1,3}|IV|V)\s*-\s*(?P<lp>[\d,]+)",
            block,
            flags=re.IGNORECASE,
        )

        if not season_match or not high_match:
            continue

        if season_match.group("season"):
            raw_season = re.sub(r"\s+", " ", season_match.group("season")).strip()
            season = f"S{raw_season}"
        else:
            season = f"S{season_match.group('old_season')} - {season_match.group('old_split')}"

        key = (season, high_match.group("tier"), high_match.group("division"), high_match.group("lp"))
        if key in seen:
            continue
        seen.add(key)
        ranks.append(
            {
                "season": season,
                "highRank": {
                    "tier": normalize_scraped_tier(high_match.group("tier"), high_match.group("division")),
                    "lp": high_match.group("lp").replace(",", ""),
                },
            }
        )

    return ranks


def crawl_sources(game_name, tag_line):
    encoded_id = quote(f"{game_name}-{tag_line}")
    sources = [
        {
            "name": "FOW.LOL",
            "url": f"https://www.fow.lol/find/{encoded_id}",
        },
        {
            "name": "OP.GG",
            "url": f"https://op.gg/ko/lol/summoners/kr/{encoded_id}?queue_type=SOLORANKED",
        },
    ]

    results = []
    for source in sources:
        try:
            html = fetch_page(source["url"])
            result = {
                **source,
                "ok": True,
                "mentions": extract_tier_mentions(html),
            }
            if source["name"] == "OP.GG":
                result["seasonRanks"] = extract_opgg_season_ranks(html)
                result["currentHighestRank"] = extract_opgg_current_highest_rank(html)
            if source["name"] == "FOW.LOL":
                result["seasonRanks"] = extract_fow_solo_ranks(html)
            results.append(result)
        except requests.RequestException as error:
            results.append({**source, "ok": False, "message": str(error)})
        except ScrapeError as error:
            results.append({**source, "ok": False, "message": str(error)})

    return results


def rank_strength(rank):
    if not rank or not rank.get("tier"):
        return -1

    tier = rank["tier"].lower().strip()
    lp = int(str(rank.get("lp") or 0).replace(",", ""))
    if tier in ["master", "grandmaster", "challenger"]:
        return 700000 + lp

    match = re.match(r"(iron|bronze|silver|gold|platinum|emerald|diamond)\s*([1-5])", tier)
    if not match:
        return -1

    tier_order = {
        "iron": 0,
        "bronze": 1,
        "silver": 2,
        "gold": 3,
        "platinum": 4,
        "emerald": 5,
        "diamond": 6,
    }
    division = int(match.group(2))
    return tier_order[match.group(1)] * 10000 + (6 - division) * 100 + lp


def choose_best_rank(ranks):
    valid_ranks = [rank for rank in ranks if rank and rank.get("tier")]
    if not valid_ranks:
        return None
    return max(valid_ranks, key=rank_strength)


def riot_rank_to_scraped_rank(entry):
    if not entry:
        return None

    tier = (entry.get("tier") or "").lower()
    division = ROMAN_DIVISIONS.get(entry.get("rank"), entry.get("rank") or "")
    if not tier:
        return None

    return {
        "tier": tier if tier in ["master", "grandmaster", "challenger"] else f"{tier} {division}",
        "lp": str(entry.get("leaguePoints") or 0),
    }


def summarize_opgg_ranks(source):
    season_ranks = source.get("seasonRanks") or []
    season_2025_2026 = []
    season_2024 = []
    all_time = []

    current_highest = source.get("currentHighestRank")
    if current_highest:
        season_2025_2026.append(current_highest)
        all_time.append(current_highest)

    for season in season_ranks:
        season_name = season.get("season", "")
        candidates = [season.get("highRank"), season.get("rank")]
        all_time.extend(candidates)
        if season_name in ["S2025", "S2026"]:
            season_2025_2026.extend(candidates)
        if season_name in ["S2024 S1", "S2024 S2", "S2024 S3"]:
            season_2024.extend(candidates)

    return {
        "best2025To2026": choose_best_rank(season_2025_2026),
        "best2024": choose_best_rank(season_2024),
        "allTimeBest": choose_best_rank(all_time),
    }


def fow_season_number(season):
    match = re.match(r"S(\d+)", season or "")
    return int(match.group(1)) if match else -1


def summarize_combined_ranks(sources, riot=None):
    opgg = next((source for source in sources if source["name"] == "OP.GG"), {})
    fow = next((source for source in sources if source["name"] == "FOW.LOL"), {})
    opgg_summary = summarize_opgg_ranks(opgg)
    fow_ranks = fow.get("seasonRanks") or []
    riot_current_solo = riot_rank_to_scraped_rank((riot or {}).get("soloRank"))

    fow_s14 = [
        season["highRank"]
        for season in fow_ranks
        if fow_season_number(season.get("season")) == 14
    ]
    fow_s15_s16 = [
        season["highRank"]
        for season in fow_ranks
        if fow_season_number(season.get("season")) in [15, 16]
    ]
    fow_s14_and_below = [
        season["highRank"]
        for season in fow_ranks
        if 1 <= fow_season_number(season.get("season")) <= 14
    ]
    best_2025_to_2026 = choose_best_rank(
        [opgg_summary["best2025To2026"], *fow_s15_s16, riot_current_solo]
    )

    return {
        "best2025To2026": best_2025_to_2026,
        "best2024": choose_best_rank(fow_s14),
        "allTimeBest": choose_best_rank(
            [best_2025_to_2026, *fow_s14_and_below]
        ),
    }
