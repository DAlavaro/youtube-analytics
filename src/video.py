import json
import os

import isodate
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class Video:
    """Класс для видео"""

    def __init__(self, video_id) -> None:
        self.video_id = video_id
        self.api_key: str = os.getenv('YOUTUBE_API')
        self.video_data = None
        self.video_data = None
        try:
            self.fetch_video_data()
        except HttpError as e:
            print(f"Error fetching video data: {e}")
            self.video_data = None


    def fetch_video_data(self):
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        video = youtube.videos().list(id=self.video_id, part='snippet,statistics,contentDetails,topicDetails').execute()
        self.video_data = json.dumps(video, indent=2, ensure_ascii=False)


    def __str__(self):
        return self.title

    def my_service(self):
        return json.loads(self.video_data)

    @property
    def title(self) -> str:
        if self.my_service()['items']:
            return self.my_service()['items'][0]['snippet']['title']
        else:
            None


    @property
    def view_count(self):
        return self.my_service()['items'][0]['statistics']['viewCount']

    @property
    def like_count(self):
        if self.my_service()['items']:
            return self.my_service()['items'][0]['statistics']['likeCount']
        return None

    @property
    def comment_count(self):
        return self.my_service()['items'][0]['statistics']['commentCount']

    @property
    def duration(self):
        duration_str = self.my_service()['items'][0]['contentDetails']['duration']
        duration = isodate.parse_duration(duration_str)
        return duration

    def url(self):
        return f'https://youtu.be/{self.video_id}'


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    @property
    def url(self):
        return f'https://www.youtube.com/playlist?list={self.playlist_id}'

