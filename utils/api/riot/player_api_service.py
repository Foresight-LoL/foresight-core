import asyncio
from datetime import datetime, UTC
from typing import Optional, cast, List, Tuple

from utils.api.riot.models.challenge import Challenge
from utils.api.riot.models.player import PlayerBase
from utils.api.riot.models.player_snapshot import PlayerSnapshot
from utils.api.riot.region import Region
from utils.api.riot.riot_api_response import RiotAPIResponse
from utils.api.riot.riot_games_api import AsyncRiotAPIClient


class PlayerApiService:
    def __init__(self, api_client: AsyncRiotAPIClient, default_region: Region):
        self.api_client = api_client
        self.default_region = default_region

    async def request_by_puuid(self, puuid: str, region: Optional[Region] = None) -> PlayerBase:
        region = region or self.default_region

        player_response = await self.api_client.request(path=f"/riot/account/v1/accounts/by-puuid/{puuid}", region=region)
        if not (isinstance(player_response.data, dict) and player_response.ok):
            raise RuntimeError(f"error or malformed response on upstream api for player response: {player_response.data}")

        player_response_json = player_response.data
        return PlayerBase.from_json(player_response_json, region=region)

    async def request_by_game_name(self, game_name: str, tag_line: str, region: Optional[Region] = None) -> PlayerBase:
        region = region or self.default_region

        player_response = await self.api_client.request(path=f"/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}", region=region)
        if not (isinstance(player_response.data, dict) and player_response.ok):
            raise RuntimeError(f"error or malformed response on upstream api for player response: {player_response.data}")

        player_response_json = player_response.data
        return PlayerBase.from_json(player_response_json, region=region)

    async def _get_player_challenges_helper(self, puuid: str, region: Optional[Region] = None) -> Tuple[List[Challenge], RiotAPIResponse]:
        region = region or self.default_region

        challenges_response = await self.api_client.request(path=f"/lol/challenges/v1/models-data/{puuid}", region=region)
        if not (isinstance(challenges_response.data, dict) and challenges_response.ok):
            raise RuntimeError(f"error or malformed response on upstream api for challenges response: {challenges_response.data}")

        return Challenge.from_json(challenges_response.data), challenges_response

    async def get_player_challenges(self, puuid: str, region: Optional[Region] = None) -> List[Challenge]:
        return (await self._get_player_challenges_helper(puuid, region))[0]

    async def _get_player_snapshot_helper(self, puuid: str, region: Optional[Region] = None) -> Tuple[PlayerSnapshot, List[Challenge]]:
        region = region or self.default_region

        summoner_response, (challenges, challenges_response) = await asyncio.gather(
            self.api_client.request(f"/lol/summoner/v4/summoners/by-puuid/{puuid}", region=region),
            self._get_player_challenges_helper(puuid, region)
        )

        if not (isinstance(summoner_response.data, dict) and summoner_response.ok and isinstance(challenges_response.data, dict) and challenges_response.ok):
            raise RuntimeError(f"error or malformed response on upstream api for player snapshot response: {summoner_response.data}")

        player_snapshot = PlayerSnapshot.from_json(puuid=puuid, summoner_json=summoner_response.data, challenges_json=challenges_response.data)

        return player_snapshot, challenges

    async def get_player_snapshot(self, puuid: str, region: Optional[Region] = None) -> PlayerSnapshot:
        return (await self._get_player_snapshot_helper(puuid, region))[0]
