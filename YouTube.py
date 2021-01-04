import youtube_dl
import json
import os
import urllib.parse
import urllib.request


class YouTube(object):
    YOUTUBE_API_SEARCH_URL = 'https://content.googleapis.com/youtube/v3/search?q={}&maxResults=1&part=snippet,id&key={}'
    YOUTUBE_VIDEO_PREFIX = 'https://www.youtube.com/watch?v='
    OPTIONS = {
        'quiet': True,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }

    def __init__(self, api_key):
        self._api_key = api_key

    def get_id_by_name(self, name):
        """
        Return the id of the youtube first video search result by video name
        :param name: The video's name
        :return: The video's id
        """
        response = urllib.request.urlopen(YouTube.YOUTUBE_API_SEARCH_URL.format(urllib.parse.quote(name),
                                                                                self._api_key)).read()
        youtube_json = json.loads(response)
        try:
            return str(youtube_json['items'][0]['id']['videoId'])
        except KeyError:
            return None

    @staticmethod
    def download_video(video_id, path, output_format='%(id)s.%(ext)s'):
        """
        Download a video from YouTube to the disk
        :param video_id: The video's ID
        :param path: The folder's path to save the file
        :param output_format: Format for the file, default of <id>.<ext>
        """
        YouTube.OPTIONS['outtmpl'] = os.path.join(path, output_format)
        downloader = youtube_dl.YoutubeDL(YouTube.OPTIONS)
        downloader.extract_info(YouTube.YOUTUBE_VIDEO_PREFIX + video_id, download=True)
