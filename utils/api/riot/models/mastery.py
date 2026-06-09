from dataclasses import dataclass
from datetime import datetime
from typing import List, Self, Optional

import polars as pl

from utils.api.riot.models.api_model_interface import APIModelInterface


@dataclass
class Mastery(APIModelInterface):
    puuid: str
    champion_id: int
    champion_points_until_next_level: int
    chest_granted: Optional[bool]
    last_play_time: datetime
    champion_level: int
    champion_points: int
    champion_points_since_last_level: int
    mark_required_for_next_level: int
    champion_season_milestone: int
    tokens_earned: int
    milestone_grades: List[str]

    @classmethod
    def to_dataframe(cls, records: List[Self]) -> pl.DataFrame:
        return pl.DataFrame(records)
