from typing import List

from .base_resource import AsyncBaseResource
from .session import AsyncSession
from models.models import ChangeLog


class Changelog(AsyncBaseResource):
    """Handles operations related to the /changelog endpoint."""
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.base_url = "/changelog"

    async def list_changelogs(self, timestamp) -> List[ChangeLog]:
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
        data = await self.session.get(self.base_url, params=params)

        return [ChangeLog(**item) for item in data]
