import requests
import json

class RadarrClient:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url

    def make_request(self, method, url, data=None):
        headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json"
        }
        if data is not None:
            data = json.dumps(data)
        response = requests.request(method, url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()

    def get_quality_profiles(self):
        url = f"{self.base_url}/api/v3/qualityProfile"
        return self.make_request("GET", url)
    
    def get_movies(self):
        url = f"{self.base_url}/api/v3/movie"
        return self.make_request("GET", url)
    
    def get_movie(self, movie_id):
        url = f"{self.base_url}/api/v3/movie/{movie_id}"
        return self.make_request("GET", url)
    
    def update_movie(self, movie_id, update_data):
        current_movie = self.get_movie(movie_id)
        # Update only the specified fields
        current_movie.update(update_data)
        url = f"{self.base_url}/api/v3/movie/{movie_id}"
        return self.make_request("PUT", url, data=current_movie)
    
    def trigger_search(self, movie_id):
        url = f"{self.base_url}/api/v3/command"
        data = {
            "name": "MoviesSearch",
            "movieIds": [movie_id]
        }
        return self.make_request("POST", url, data=data)
    
