from .base_resource import BaseResource

class Teams(BaseResource):
    """Handles operations related to the /teams endpoint."""
    def __init__(self, session):
        super().__init__(session)
        self.base_url = "/teams"

    def list_teams(self, skip=None, take=None, order_by=None, search=None):
        """
        Fetches a list of teams with optional pagination, sorting, and search.

        Args:
            skip (int, optional): Number of records to skip.
            take (int, optional): Number of records to retrieve. <--- Doc updated
                                  (API spec previously noted default of 100 for limit, may apply to take).
            order_by (str, optional): Field and direction to sort by (e.g., "name ASC").
            search (str, optional): Search term for team names.

        Returns:
            list: A list of team objects.
        """
        return self.list(skip=skip, take=take, order_by=order_by, search=search)

    def get_team(self, team_id):
        """
        Fetches a single team by its ID.

        Args:
            team_id (int): The unique ID of the team.

        Returns:
            dict: The team details.
        """
        return self.get(team_id)

    def get_team_players(self, team_id):
        """
        Fetches a team's details including its players.

        Args:
            team_id (int): The unique ID of the team.

        Returns:
            list: A list containing the team object with an embedded list of player objects.
                  (Note: API spec shows array response, likely wrapping the TeamWithPlayers schema).
        """
        return self.session.get(f"{self.base_url}/{team_id}/players")