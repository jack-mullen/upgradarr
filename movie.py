from datetime import datetime, timedelta
import time
from typing import Dict
from zoneinfo import ZoneInfo

import logging

logger = logging.getLogger(__name__)

class Movie:
    def __init__(self, movie_data: dict, quality_profiles: Dict[str, int], config):
        self.movie_data = movie_data
        self.quality_profiles = quality_profiles
        self.config = config

    @property
    def title(self) -> str:
        return self.movie_data['title']

    @property
    def id(self) -> int:
        return self.movie_data['id']

    @property
    def current_profile_id(self) -> int:
        return self.movie_data['qualityProfileId']

    @property
    def current_profile_name(self) -> str:
        # Find the profile name that matches the current ID
        for name, id in self.quality_profiles.items():
            if id == self.current_profile_id:
                return name
        return 'Unknown'

    @property
    def added_date(self) -> datetime:
        return datetime.fromisoformat(self.movie_data['added'].replace('Z', '+00:00'))

    def determine_matching_profile(self) -> str:
        profiles = self.config.get_profiles()
        
        logger.debug(f"Determining profile for movie: {self.title} (Added: {self.added_date})")
        logger.debug(f"Available profile priority: {list(profiles.keys())}")
        
        for profile_name, profile_config in profiles.items():
            if not profile_config or profile_config['active_until_days'] is None:
                logger.debug(f"{self.title} added date ({self.added_date}) cannot match any other profile, so it must use profile {profile_name}")
                return profile_name
            
            active_until_days = datetime.now(ZoneInfo('UTC')) - timedelta(days=profile_config['active_until_days'])
            if self.added_date >= active_until_days:
                logger.debug(f"{self.title} added date ({self.added_date}) is within active period for profile {profile_name}")
                return profile_name
            else:
                logger.debug(f"{self.title} added date ({self.added_date}) is too old for profile {profile_name}")
        
        raise ValueError("No matching profile found")

    def process(self, radarr_client) -> None:
        try:
            matching_profile_name = self.determine_matching_profile()
            matching_profile_id = self.quality_profiles.get(matching_profile_name)

            if matching_profile_id != self.current_profile_id:
                logger.info(
                    f"Updating quality profile for {self.title} "
                    f"from {self.current_profile_name} to {matching_profile_name}"
                )
                radarr_client.update_movie(self.id, {'qualityProfileId': matching_profile_id})
                logger.info(f"Triggering search for {self.title}")
                radarr_client.trigger_search(self.id)
                time.sleep(1)  # Rate limiting
            else:
                logger.debug(
                    f"No change for {self.title}, "
                    f"{self.current_profile_name} is still the best profile"
                )
        except Exception as e:
            logger.error(f"Error processing movie {self.title}: {str(e)}") 