import os
from YouTube import YouTube


"""
A code for downloading bulk songs from youtube by songs names

Omri Maor - u122
"""


YOUTUBE_API_KEY = 'AIzaSyD7JJgCoo-Qdi_-dTQPn4pd9wXZPQdlD9w'
OUTPUT_PATH = 'songs/'


def get_songs(path='Songs.txt'):
    """
    An generator that returns each time a different song from the list until the end
    :param path: The path to the songs file
    :return: A different song from the list (by order)
    """
    with open(path, 'r') as songs_file:
        for line in songs_file:
            if line.strip() != '':
                yield line.strip()


def main():
    youtube = YouTube(YOUTUBE_API_KEY)
    try:
        for song in get_songs():
            print 'Downloading {}'.format(song)
            video_id = youtube.get_id_by_name(song)
            if video_id is None:
                print '\tCouldn\'t find this video on YouTube'
            elif os.path.exists(os.path.join(OUTPUT_PATH, video_id) + YouTube.OUTPUT_FORMAT):
                print '\tSong already downloaded'
            else:
                youtube.download_video(video_id, OUTPUT_PATH)
    except Exception as e:
        print str(e)


if __name__ == '__main__':
    main()
