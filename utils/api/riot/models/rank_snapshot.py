from dataclasses import dataclass
from datetime import date
from typing import List, Self

import polars as pl

from utils.api.riot.models.api_model_interface import APIModelInterface


@dataclass
class RankSnapshot(APIModelInterface):
    puuid: str
    queue_type: str
    snapshot_date: date
    tier: str
    rank: str
    league_points: int
    wins: int
    losses: int
    hot_streak: bool
    veteran: bool
    fresh_blood: bool
    inactive: bool

    @classmethod
    def to_dataframe(cls, records: List[Self]) -> pl.DataFrame:
        return pl.DataFrame(records)