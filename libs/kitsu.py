import requests

class Kitsu:
    def __init__(self):
        self.base_url = "https://kitsu.io/api/edge/"

    def get_anime_info(self, anime_id):
        try:
            response = requests.get(f"{self.base_url}anime/{anime_id}")
            if response.status_code == 200:
                return response.json()
            return None, "Failed to fetch anime info"
        except Exception as e:
            return None, str(e)
