import requests
from datetime import datetime, timedelta

class APIClient:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = "https://api.b2broker.com/auth/token"
        self.client_url = "https://api.b2broker.com/back-office/v2/clients"
        self.token = self.get_token()
    
    def get_token(self) -> str:
        response = requests.post(self.token_url, data={
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        })
        response.raise_for_status()
        return response.json()['access_token']

    def refresh_token(self):
        self.token = self.get_token()

    def get_clients(self, from_update_time: datetime, to_update_time: datetime) -> list:
        headers = {'Authorization': f'Bearer {self.token}'}
        params = {
            'fromUpdateTime': from_update_time.isoformat(),
            'toUpdateTime': to_update_time.isoformat()
        }
        response = requests.get(self.client_url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()['data']
