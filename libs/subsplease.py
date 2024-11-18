import feedparser

class SubsPlease:
    def __init__(self, rss_url):
        self.rss_url = rss_url

    def get_latest_episode(self):
        try:
            feed = feedparser.parse(self.rss_url)
            latest_episode = feed.entries[0]
            return latest_episode
        except Exception as e:
            return None, str(e)
