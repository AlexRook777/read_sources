import read_youtube_subtitle, read_youtube_playlist
import json
from pathlib import Path
import re
import sys

def save_youtube_subtitels_to_file(list_of_playlists_to_save=[]):
    """
    Example how to read this file
        file_path = Path('youtube_subtitles.json')
        with open(file_path, 'r', encoding='koi8-u') as json_file:
            loaded_data = json.load(json_file)
    """
    # Save subtiteles to a JSON file
    if list_of_playlists_to_save:
        print("Info: Saving subtitles to file") 
        try:
            file_path = Path('youtube_subtitles.json')
            with file_path.open('w', encoding='utf-8') as f:
                json.dump(list_of_playlists_to_save, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving subtitles to file: {repr(e)}")
    
    
if __name__ == "__main__":
    
    #sys.exit(0)

    list_of_playlists_to_process = [\
        'https://www.youtube.com/playlist?list=PL4sbV49yxRUhtG1BxSqD-PrnUBbXB2_06',\
        'https://www.youtube.com/playlist?list=PL1W2RXCJBBmVWj-mXii6fa5rJyJnr1QX5'\
    ]
    list_of_playlist_to_save = []
    for playlist_url in list_of_playlists_to_process:
        playlist_videos = read_youtube_playlist.get_youtube_playlist(playlist_url)
        if playlist_videos:
            print(f"Found {len(playlist_videos)} video(s) in playlist")
            for video in playlist_videos: 
                subtitles_text = read_youtube_subtitle.get_youtube_subtitles(video['url'], lang_codes=['ru', 'uk', 'en', 'a.en', 'uk', 'a.uk']) 
                subtitles_text = subtitles_text if subtitles_text else ""
                video['subtitles'] = subtitles_text
                if subtitles_text:
                    list_of_playlist_to_save.append(video)
                    print(f"Title: {video['title']}\n      ID: {video['id']}\n      URL: {video['url']}\n      Subtitles: {video['subtitles'][:100]}")
                
        else:
            print("Error")
    

    save_youtube_subtitels_to_file(list_of_playlist_to_save)
