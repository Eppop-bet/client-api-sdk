from .base_resource import BaseResource


class Changelog(BaseResource):
    """Handles operations related to the /changelog endpoint."""
    def __init__(self, session):
        super().__init__(session)
        self.base_url = "/changelog"

    def list_changelogs(self, timestamp):
        """
        Fetches changelog entries since a specific timestamp.

        Args:
            timestamp (str): ISO 8601 formatted date-time string.
                             Only changes occurring after this time will be returned.

        Returns:
            list: A list of changelog entries.
        """
        if not timestamp:
            raise ValueError("The 'timestamp' parameter is required.")

        params = {"timestamp": timestamp}
        return self.session.get(self.base_url, params=params)
