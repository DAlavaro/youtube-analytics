import json
import os
from datetime import timedelta

from googleapiclient.discovery import build

from src.video import Video


class PlayList:
    """Класс для плейлиста"""

    def __init__(self, playlist_id) -> None:
        self.playlist_id = playlist_id

        self.api_key: str = os.getenv('YOUTUBE_API')
        self.video_data = None
        self.fetch_playlist_data()

    def fetch_playlist_data(self):
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        playlist = youtube.playlists().list(id=self.playlist_id, part='snippet, contentDetails').execute()
        self.playlist_data = json.dumps(playlist, indent=2, ensure_ascii=False)


    @property
    def title(self):
        return json.loads(self.playlist_data)['items'][0]['snippet']['title']

    @property
    def url(self):
        return f'https://www.youtube.com/playlist?list={self.playlist_id}'

    @property
    def total_duration(self):
        total_duration = timedelta()

        youtube = build('youtube', 'v3', developerKey=self.api_key)
        playlist_items = youtube.playlistItems().list(playlistId=self.playlist_id, part='snippet, contentDetails').execute()
        video_ids = [item['contentDetails']['videoId'] for item in playlist_items['items']]

        for video_id in video_ids:
            video = Video(video_id)
            duration = video.duration
            total_duration += duration
        return total_duration

    def show_best_video(self):
        best_video = None
        max_likes = 0

        youtube = build('youtube', 'v3', developerKey=self.api_key)
        playlist_items = youtube.playlistItems().list(playlistId=self.playlist_id, part='contentDetails').execute()
        video_ids = [item['contentDetails']['videoId'] for item in playlist_items['items']]

        for video_id in video_ids:
            video = Video(video_id)
            likes = int(video.like_count)
            if likes > max_likes:
                max_likes = likes
                best_video = video

        return best_video.url() if best_video else None





