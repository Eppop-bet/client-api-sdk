class BaseResource:
    """
    Base class for API resource interactions.

    Provides common methods for fetching lists and individual items.
    """
    def __init__(self, session):
        """
        Initializes the resource with an active session.

        Args:
            session (Session): The authenticated session object.
        """
        self.session = session
        self.base_url = ""  # Must be overridden by subclasses

    def _build_common_params(self, params, skip=None, take=None, order_by=None, search=None):
        """
        Helper to add common query parameters to a dictionary.

        Args:
            params (dict): The dictionary to add parameters to.
            skip (int, optional): Number of records to skip.
            take (int, optional): Number of records to retrieve.
            order_by (dict, optional): Sorting order. Example: {"name": "asc"}.
                                       Requests library handles encoding (e.g., orderBy[name]=asc).
            search (str, optional): Search term.

        Returns:
            dict: The updated parameters' dictionary.
        """
        if skip is not None:
            params["skip"] = skip
        if take is not None:
            params["take"] = take
        if order_by:
            params["orderBy"] = order_by
        if search:
            params["search"] = search
        return params

    def list(self, skip=None, take=None, order_by=None, search=None):
        """
        Fetches a list of resources using common query parameters.

        Note: Subclasses might need to override this if they use different
              or additional query parameters not covered here.

        Args:
            skip (int, optional): Number of records to skip for pagination.
            take (int, optional): Number of records to retrieve. <--- Changed from limit
            order_by (dict, optional): Field and direction to sort by. Example: {"name": "asc"}.
            search (str, optional): Search term to filter results.

        Returns:
            list: A list of resource items.
        """
        if not self.base_url:
            raise NotImplementedError("Subclasses must define self.base_url")

        params = self._build_common_params({}, skip=skip, take=take, order_by=order_by, search=search)
        return self.session.get(self.base_url, params=params)

    def get(self, resource_id):
        """
        Fetches a single resource by its ID.

        Args:
            resource_id (int or str): The unique identifier of the resource.

        Returns:
            dict: The resource details.
        """
        if not self.base_url:
            raise NotImplementedError("Subclasses must define self.base_url")

        return self.session.get(f"{self.base_url}/{resource_id}")
