import logging
from typing import Dict

from requests import HTTPError

from configuration import RadarrConfig
from radarr import RadarrClient
from movie import Movie

config = RadarrConfig()

log_level = getattr(logging, config.get_config().get('log_level', 'INFO').upper())
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def initialize_radarr_client() -> RadarrClient:
    radarr_config = config.get_radarr_config()
    api_key = radarr_config.get('api_key')
    base_url = radarr_config.get('base_url')
    
    if not api_key or not base_url:
        raise ValueError("api_key and base_url must be set in config.yaml")
    
    return RadarrClient(api_key=api_key, base_url=base_url)

def get_quality_profiles(radarr: RadarrClient) -> Dict[str, int]:
    profiles = radarr.get_quality_profiles()
    return {profile['name']: profile['id'] for profile in profiles}

def main() -> None:
    try:
        radarr_client = initialize_radarr_client()
        
        quality_profiles = get_quality_profiles(radarr_client)
        movies = radarr_client.get_movies()
        
        logger.info(f"Found {len(movies)} movies, processing...")

        if len(movies) == 0:
            logger.warning("No movies found, exiting.")
            return
        
        for movie_data in movies:
            movie = Movie(movie_data, quality_profiles, config)
            movie.process(radarr_client)
        
        logger.info("Quality profile updates and searches completed")
    except HTTPError as e:
        logger.error(f"An error occured when making a request to Radarr: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()