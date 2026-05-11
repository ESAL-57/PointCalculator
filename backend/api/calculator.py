POSITIONS = [
    ("top", "탑"),
    ("jungle", "정글"),
    ("mid", "미드"),
    ("adc", "원딜"),
    ("support", "서폿"),
]

POSITION_LABELS = dict(POSITIONS)
POINT_LIMIT = 165

TIER_POINTS = {
    "마/그/챌 1800 이상": {"top": 67, "jungle": 66, "mid": 62, "adc": 65, "support": 52},
    "마/그/챌 1700 ~ 1799": {"top": 66, "jungle": 64.3, "mid": 61.1, "adc": 64.7, "support": 51.5},
    "마/그/챌 1600 ~ 1699": {"top": 65.5, "jungle": 63.8, "mid": 60.8, "adc": 64.4, "support": 50.9},
    "마/그/챌 1500 ~ 1599": {"top": 64.6, "jungle": 63.3, "mid": 59.9, "adc": 64.2, "support": 50.6},
    "마/그/챌 1400 ~ 1499": {"top": 63.8, "jungle": 62.2, "mid": 58.2, "adc": 63.9, "support": 50.1},
    "마/그/챌 1300 ~ 1399": {"top": 63.1, "jungle": 61.3, "mid": 57.3, "adc": 63.3, "support": 49.8},
    "마/그/챌 1200 ~ 1299": {"top": 62.4, "jungle": 60.5, "mid": 56, "adc": 62.7, "support": 49.3},
    "마/그/챌 1100 ~ 1199": {"top": 59.9, "jungle": 59.4, "mid": 54.7, "adc": 62.2, "support": 48.7},
    "마/그/챌 1000 ~ 1099": {"top": 57.8, "jungle": 57.7, "mid": 53.1, "adc": 61.3, "support": 48},
    "마/그/챌 900 ~ 999": {"top": 54.8, "jungle": 55.4, "mid": 51.4, "adc": 58.8, "support": 46.2},
    "마/그/챌 800 ~ 899": {"top": 52.6, "jungle": 53.1, "mid": 50.2, "adc": 56.1, "support": 44.5},
    "마/그/챌 700 ~ 799": {"top": 51.3, "jungle": 50.6, "mid": 49.3, "adc": 53.7, "support": 42.8},
    "마/그/챌 600 ~ 699": {"top": 49.7, "jungle": 48.4, "mid": 48, "adc": 51.1, "support": 41.1},
    "마/그/챌 500 ~ 599": {"top": 47.9, "jungle": 46.3, "mid": 46.2, "adc": 48.6, "support": 39},
    "마/그/챌 400 ~ 499": {"top": 45.2, "jungle": 44.3, "mid": 45.2, "adc": 46.2, "support": 37.7},
    "마/그/챌 300 ~ 399": {"top": 43, "jungle": 42.4, "mid": 44.7, "adc": 43.5, "support": 36.1},
    "마/그/챌 200 ~ 299": {"top": 41.8, "jungle": 40.6, "mid": 43, "adc": 40.6, "support": 35},
    "마/그/챌 100 ~ 199": {"top": 39.1, "jungle": 39.4, "mid": 41.3, "adc": 38.3, "support": 34},
    "마/그/챌 0 ~ 99": {"top": 37.4, "jungle": 38.2, "mid": 39.8, "adc": 36.1, "support": 33.1},
    "다이아1": {"top": 35.7, "jungle": 36.8, "mid": 38.7, "adc": 34, "support": 32.2},
    "다이아2": {"top": 33.8, "jungle": 34.8, "mid": 38, "adc": 32.1, "support": 31.3},
    "다이아3": {"top": 31.6, "jungle": 32.5, "mid": 37.1, "adc": 29.7, "support": 30.3},
    "다이아4": {"top": 30.3, "jungle": 30.7, "mid": 35.4, "adc": 27.6, "support": 29.3},
    "에메랄드1": {"top": 28.6, "jungle": 28.8, "mid": 34.6, "adc": 25.7, "support": 28.2},
    "에메랄드2": {"top": 27.3, "jungle": 26.6, "mid": 33, "adc": 24.3, "support": 27},
    "에메랄드3": {"top": 26.5, "jungle": 24.8, "mid": 31.8, "adc": 22.8, "support": 26},
    "에메랄드4": {"top": 26, "jungle": 23.4, "mid": 29.6, "adc": 21.6, "support": 25.1},
    "플래티넘1": {"top": 25.2, "jungle": 21.9, "mid": 27.1, "adc": 20.3, "support": 24.2},
    "플래티넘2": {"top": 24.7, "jungle": 20.5, "mid": 24.3, "adc": 18.7, "support": 22.8},
    "플래티넘3": {"top": 24, "jungle": 19.3, "mid": 22.7, "adc": 17.5, "support": 22},
    "플래티넘4": {"top": 21.2, "jungle": 18.1, "mid": 21.1, "adc": 16.4, "support": 21.2},
    "골드1": {"top": 19, "jungle": 16.7, "mid": 19.7, "adc": 15.1, "support": 20.5},
    "골드2": {"top": 17.7, "jungle": 14.7, "mid": 17.8, "adc": 13.4, "support": 19.1},
    "골드3": {"top": 15.9, "jungle": 13.8, "mid": 16.8, "adc": 12.6, "support": 18.3},
    "골드4": {"top": 14.6, "jungle": 12.8, "mid": 15.9, "adc": 11.9, "support": 17.6},
    "실버1": {"top": 13, "jungle": 11.9, "mid": 14.8, "adc": 11.3, "support": 16.7},
    "실버2": {"top": 12, "jungle": 11, "mid": 13.9, "adc": 10.6, "support": 15.9},
    "실버3 이하": {"top": 11, "jungle": 10, "mid": 13, "adc": 10, "support": 15},
}

TIER_ORDER = list(TIER_POINTS.keys())
TIER_STRENGTH = {tier: len(TIER_ORDER) - index for index, tier in enumerate(TIER_ORDER)}
POINT_GROUPS = {
    "low": {"label": "실버1 이하 ~ 플래티넘1", "small": 1, "large": 2},
    "middle": {"label": "에메랄드4 ~ 다이아1", "small": 3, "large": 4},
    "master": {"label": "마스터 0점 이상", "small": 4, "large": 6},
}

LOWER_BOUND_RULES = [
    (["마/그/챌 400 ~ 499", "마/그/챌 500 ~ 599", "마/그/챌 600 ~ 699", "마/그/챌 700 ~ 799", "마/그/챌 800 ~ 899", "마/그/챌 900 ~ 999", "마/그/챌 1000 ~ 1099", "마/그/챌 1100 ~ 1199", "마/그/챌 1200 ~ 1299", "마/그/챌 1300 ~ 1399", "마/그/챌 1400 ~ 1499", "마/그/챌 1500 ~ 1599", "마/그/챌 1600 ~ 1699", "마/그/챌 1700 ~ 1799", "마/그/챌 1800 이상"], "마/그/챌 200 ~ 299"),
    (["마/그/챌 200 ~ 299", "마/그/챌 300 ~ 399"], "마/그/챌 0 ~ 99"),
    (["마/그/챌 0 ~ 99", "마/그/챌 100 ~ 199"], "다이아4"),
    (["다이아1", "다이아2", "다이아3", "다이아4"], "에메랄드4"),
    (["에메랄드1", "에메랄드2", "에메랄드3", "에메랄드4"], "플래티넘4"),
    (["플래티넘1", "플래티넘2", "플래티넘3", "플래티넘4"], "골드4"),
]


def normalize_tier(tier):
    if not tier:
        return tier
    tier = (
        tier.replace("IV", "4")
        .replace("III", "3")
        .replace("II", "2")
        .replace("I", "1")
    )
    if tier.startswith("아이언") or tier.startswith("브론즈"):
        return "실버3 이하"
    if tier in ["실버3", "실버4"]:
        return "실버3 이하"
    return tier


def options_payload():
    return {
        "positions": [{"value": value, "label": label} for value, label in POSITIONS],
        "tiers": TIER_ORDER,
        "pointLimit": POINT_LIMIT,
        "rankTiers": [
            {"value": "IRON", "label": "아이언", "divisions": ["4", "3", "2", "1"]},
            {"value": "BRONZE", "label": "브론즈", "divisions": ["4", "3", "2", "1"]},
            {"value": "SILVER", "label": "실버", "divisions": ["4", "3", "2", "1"]},
            {"value": "GOLD", "label": "골드", "divisions": ["4", "3", "2", "1"]},
            {"value": "PLATINUM", "label": "플래티넘", "divisions": ["4", "3", "2", "1"]},
            {"value": "EMERALD", "label": "에메랄드", "divisions": ["4", "3", "2", "1"]},
            {"value": "DIAMOND", "label": "다이아", "divisions": ["4", "3", "2", "1"]},
            {"value": "MASTER_PLUS", "label": "마스터 이상", "usesLp": True},
        ],
    }


def stronger_tier(tier_a, tier_b):
    return tier_a if TIER_STRENGTH[tier_a] >= TIER_STRENGTH[tier_b] else tier_b


def lower_bound_for(achieved_tier):
    for tiers, lower_bound in LOWER_BOUND_RULES:
        if achieved_tier in tiers:
            return lower_bound
    return None


def effective_tier(participant_tier, achieved_tier):
    lower_bound = lower_bound_for(achieved_tier)
    if not lower_bound:
        return participant_tier, lower_bound, False

    adjusted = stronger_tier(participant_tier, lower_bound)
    return adjusted, lower_bound, adjusted != participant_tier


def drop_group(tier):
    strength = TIER_STRENGTH[tier]
    if strength >= TIER_STRENGTH["마/그/챌 0 ~ 99"]:
        return "master"
    if strength >= TIER_STRENGTH["에메랄드4"]:
        return "middle"
    return "low"


def drop_penalty(current_tier, previous_peak_tier):
    drop_count = TIER_ORDER.index(current_tier) - TIER_ORDER.index(previous_peak_tier)
    if drop_count <= 0:
        return 0, 0, None

    group = drop_group(current_tier)
    penalty_type = "small" if drop_count <= 3 else "large"
    return POINT_GROUPS[group][penalty_type], drop_count, POINT_GROUPS[group]["label"]


def calculate_player(player):
    position = player.get("position")
    participant_tier = normalize_tier(player.get("participantTier"))
    achieved_tier = normalize_tier(player.get("achievedTier") or participant_tier)
    previous_peak_tier = normalize_tier(player.get("previousPeakTier") or participant_tier)

    if position not in POSITION_LABELS:
        raise ValueError("포지션을 선택해주세요.")
    for tier in [participant_tier, achieved_tier, previous_peak_tier]:
        if tier not in TIER_POINTS:
            raise ValueError("티어를 선택해주세요.")

    tier, lower_bound, adjusted = effective_tier(participant_tier, achieved_tier)
    base_points = TIER_POINTS[tier][position]
    penalty, drop_count, penalty_group = drop_penalty(participant_tier, previous_peak_tier)
    total = round(base_points + penalty, 1)

    warnings = []
    if adjusted:
        warnings.append(f"참가 티어 대신 하한티어 {lower_bound} 적용")
    if penalty:
        warnings.append(f"14시즌 대비 {drop_count}티어 하락 패널티 +{penalty}")

    return {
        "name": player.get("name") or POSITION_LABELS[position],
        "position": position,
        "positionLabel": POSITION_LABELS[position],
        "participantTier": participant_tier,
        "achievedTier": achieved_tier,
        "previousPeakTier": previous_peak_tier,
        "effectiveTier": tier,
        "lowerBoundTier": lower_bound,
        "penaltyBasisTier": participant_tier,
        "basePoints": base_points,
        "dropPenalty": penalty,
        "dropCount": drop_count,
        "dropPenaltyGroup": penalty_group,
        "totalPoints": total,
        "warnings": warnings,
    }


def calculate_player_positions(player):
    return {
        "name": player.get("name") or "",
        "gameName": player.get("gameName") or "",
        "tagLine": player.get("tagLine") or "",
        "positions": [
            calculate_player({**player, "position": position})
            for position, _label in POSITIONS
        ],
    }


def calculate_team(players):
    if len(players) != 5:
        raise ValueError("팀은 5명이어야 합니다.")

    results = [calculate_player(player) for player in players]
    total = round(sum(player["totalPoints"] for player in results), 1)
    remaining = round(POINT_LIMIT - total, 1)

    return {
        "players": results,
        "totalPoints": total,
        "pointLimit": POINT_LIMIT,
        "remainingPoints": remaining,
        "isValid": total <= POINT_LIMIT,
        "warnings": [] if total <= POINT_LIMIT else [f"팀 총점이 {abs(remaining):.1f}점 초과했습니다."],
    }
