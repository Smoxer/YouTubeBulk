#!/usr/bin/python3

import os
import argparse
from YouTube import YouTube


DEFAULT_OUTPUT_FOLDER = 'songs/'
DEFAULT_FILE_FORMAT = '%(title)s.%(ext)s'
FILE_EXT = '.mp3'


def get_songs(file_path):
    """
    An generator that returns each time a different song from the list until the end
    :param file_path: The path to the songs file
    :return: A different song from the list (by order)
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'File {file_path} was not found')
    with open(file_path, 'rb') as songs_file:
        for line in songs_file:
            if line.strip() != b'':
                yield line.strip().decode('utf8')


def parse_args():
    parser = argparse.ArgumentParser(description='Automatic Youtube downloader')
    parser.add_argument('api_key', action='store', help='Set Youtube API key')
    parser.add_argument('input_file', action='store', help='Set input file')
    parser.add_argument('-o', '--output_folder', action='store', help='Set output folder', default=DEFAULT_OUTPUT_FOLDER)
    parser.add_argument('-f', '--file_format', action='store', help='Set output file format',
                        default=DEFAULT_FILE_FORMAT)
    return parser.parse_args()


def main():
    args = parse_args()
    youtube = YouTube(args.api_key)
    try:
        for song in get_songs(args.input_file):
            print(f'Downloading {song}')
            video_id = youtube.get_id_by_name(song)
            if video_id is None:
                print("\tCouldn't find this video on YouTube")
            elif os.path.exists(os.path.join(args.output_folder, video_id) + FILE_EXT):
                print('\tSong already downloaded')
            else:
                if not os.path.exists(args.output_folder):
                    os.mkdir(args.output_folder)
                if not os.path.isdir(args.output_folder):
                    raise RuntimeError(f'{args.output_folder} is not a folder!')
                youtube.download_video(video_id, args.output_folder, args.file_format)
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    main()
