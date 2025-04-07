class BaseResource:
    def __init__(self, session):
        self.session = session
        self.base_url = ""

    def _build_query_params(self, skip=None, limit=None, order_by=None, search=None):
        params = {}

        if skip is not None:
            params["skip"] = skip
        if limit is not None:
            params["limit"] = limit
        if order_by:
            params["orderBy"] = order_by
        if search:
            params["search"] = search

        return params

    def list(self, skip=None, limit=None, order_by=None, search=None):
        params = self._build_query_params(skip, limit, order_by, search)
        return self.session.get(self.base_url, params=params)

    def get(self, resource_id):
        return self.session.get(f"{self.base_url}/{resource_id}")
