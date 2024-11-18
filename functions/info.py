class AnimeInfo:
    def __init__(self, anime_name, episode_number, season):
        self.anime_name = anime_name
        self.episode_number = episode_number
        self.season = season

    async def rename(self, is_original):
        # Renaming logic here
        if is_original:
            return f"{self.anime_name} - S{self.season}E{self.episode_number}.mp4"
        return f"{self.anime_name} - {self.episode_number}.mp4"

    async def get_poster(self):
        # Logic to fetch anime poster
        return "anime_poster_url"
