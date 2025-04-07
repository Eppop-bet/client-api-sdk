from .base_resource import BaseResource


class Maps(BaseResource):
    def __init__(self, session):
        super().__init__(session)
        self.base_url = "/maps"

    def list_maps(self, **kwargs):
        return self.list(**kwargs)

    def get_map(self, map_id):
        return self.get(map_id)
