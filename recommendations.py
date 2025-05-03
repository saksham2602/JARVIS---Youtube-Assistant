import googleapiclient.discovery
from config import YOUTUBE_API_KEY

class Recommendation:
    def __init__(self):
        self.api_key = YOUTUBE_API_KEY
        self.youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=self.api_key)
    
    def get_recommendations(self):
        request = self.youtube.search().list(
            part="snippet",
            type="video",
            order="viewCount",
            maxResults=5
        )
        response = request.execute()

        return [item['snippet']['title'] for item in response['items']]

    def search_youtube(self, query):
        request = self.youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=5
        )
        response = request.execute()

        results = []
        for item in response['items']:
            title = item['snippet']['title']
            url = f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            results.append((title, url))
        return results
