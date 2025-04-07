
import requests

class Session:
    def __init__(self, base_url, email=None, password=None):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.token = None
        self.expiration_time = None

        if email and password:
            self.login(email, password)

    def login(self, email, password):
        response = self.post('/auth/sign-in', json={
            'email': email,
            'password': password
        })

        self.token = response.get('AccessToken')
        if not self.token:
            raise Exception("Login failed: AccessToken not found in response")

        self.expiration_time = response.get('ExpiresIn')
        self.session.headers.update({'Authorization': self.token})

        return response

    def _request(self, method, path, **kwargs):
        url = f"{self.base_url}/{path.lstrip('/')}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()

    def get(self, path, **kwargs):
        return self._request('GET', path, **kwargs)

    def post(self, path, **kwargs):
        return self._request('POST', path, **kwargs)

    def put(self, path, **kwargs):
        return self._request('PUT', path, **kwargs)

    def delete(self, path, **kwargs):
        return self._request('DELETE', path, **kwargs)