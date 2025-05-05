from typing import List

from .base_resource import BaseResource
from .session import Session
from ..models.models import Team, TeamWithPlayers


class Teams(BaseResource):
    """Handles operations related to the /teams endpoint."""
    def __init__(self, session: Session):
        super().__init__(session)
        self.base_url = "v1/teams"

    def list_teams(self, skip=None, take=None, order_by=None, search=None) -> List[Team]:
        """
        Fetches a list of teams with optional pagination, sorting, and search.

        Args:
            skip (int, optional): Number of records to skip.
            take (int, optional): Number of records to retrieve.
            order_by (dict, optional): Field and direction to sort by (e.g., {"name": "asc"}).
            search (str, optional): Search term for team names.

        Returns:
            list: A list of team objects.
        """
        params = self._build_common_params({}, skip=skip, take=take, order_by=order_by, search=search)
        data = self.session.get(self.base_url, params=params)
        return [Team(**item) for item in data]

    def get_team(self, team_id) -> Team:
        """
        Fetches a single team by its ID.

        Args:
            team_id (int): The unique ID of the team.

        Returns:
            dict: The team details.
        """
        data = self.get(team_id)
        return Team(**data)

    def get_team_players(self, team_id) -> List[TeamWithPlayers]:
        """
        Fetches a team's details including its players.

        Args:
            team_id (int): The unique ID of the team.

        Returns:
            list: A list containing the team object with an embedded list of player objects.
                  (Note: API spec shows array response, likely wrapping the TeamWithPlayers schema).
        """
        data = self.session.get(f"{self.base_url}/{team_id}/players")
        return [TeamWithPlayers(**item) for item in data]
