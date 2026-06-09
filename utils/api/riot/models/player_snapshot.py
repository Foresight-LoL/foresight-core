from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Self, Dict

import polars as pl

from utils.api.riot.models.challenge import ChallengeTotalPointsDTO
from utils.api.riot.models.api_model_interface import APIModelInterface


@dataclass
class PlayerSnapshot(APIModelInterface):
    puuid: str
    snapshot_date: datetime
    summoner_level: int
    title: Optional[str]
    profile_icon_id: int
    crest_border: Optional[str]
    banner_accent: Optional[str]
    prestige_crest_border: Optional[int]
    total_points: ChallengeTotalPointsDTO

    @classmethod
    def to_dataframe(cls, records: List[Self]) -> pl.DataFrame:
        return pl.DataFrame(records)

    @classmethod
    def from_json(cls, puuid: str, summoner_json: Dict, challenges_json: Dict) -> PlayerSnapshot:
        total_points_dto = ChallengeTotalPointsDTO.from_json(challenges_json)
        challenges_preferences_json = challenges_json["preferences"]

        return PlayerSnapshot(
            puuid=puuid,
            snapshot_date=datetime.today(),
            summoner_level=summoner_json["summonerLevel"],
            title=challenges_preferences_json.get("title"),
            profile_icon_id=summoner_json["profileIconId"],
            crest_border=challenges_preferences_json.get("crestBorder"),
            banner_accent=challenges_preferences_json.get("bannerAccent"),
            prestige_crest_border=challenges_preferences_json.get("prestigeCrestBorder"),
            total_points=total_points_dto
        )
