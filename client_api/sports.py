from .base_resource import BaseResource


class Sports(BaseResource):
    def __init__(self, session):
        super().__init__(session)
        self.base_url = "/sports"

    def list_sports(self, **kwargs):
        return self.list(**kwargs)

    def get_sport(self, sport_id):
        return self.get(sport_id)