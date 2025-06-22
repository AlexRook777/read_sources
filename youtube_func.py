from youtube_transcript_api._api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
from pathlib import Path
import re
from pytube import YouTube

def get_youtube_video_title(video_url: str) -> str | None:
    """
    Отримує назву YouTube відео за його URL за допомогою Pytube.

    Аргументи:
        video_url (str): URL YouTube відео.

    Повертає:
        str: Назва відео, або None у разі помилки.
    """
    try:
        yt = YouTube(video_url)
        #return clean_string_keep_cyrillic_alphanumeric_and_space(yt.title)
        return yt.title
    except Exception as e:
        print(f"Помилка при отриманні назви відео: {e}")
        return None


def save_youtube_captions_to_file(list_of_playlists_to_save=[]):
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

def clean_string_keep_cyrillic_alphanumeric_and_space(text: str) -> str:
    filtered_chars = [char for char in text if char.isalnum() or char.isspace()]
    cleaned_text_step1 = "".join(filtered_chars)
    cleaned_text_step2 = re.sub(r'\s+', ' ', cleaned_text_step1).strip()
    return cleaned_text_step2

def get_youtube_playlist(playlist_url: str, api_key='AIzaSyBWgU_1YFk9DzLLk0A_ooV_YFRjutGbCXk') -> list:
    ''' 
    Get list of video from youtube playlist
    
    Input: 
        - playlist_url - text string with full url to youtube playlist
        - api_key - Google API key

    Output:
        playlist_videos - list of dictionaries with the keys: title, id, url

    Example to call:
        if playlist_videos:
            print(f"Found {len(playlist_videos)} video(s) in playlist")
            for video in playlist_videos: 
                print(f"Title: {video['title']}      ID: {video['id']}      URL: {video['url']}")
        else:
            print("Playlist is empty")
    '''
    if not api_key:
        print("Error: No YouTube Data API Key.")
        return []

    # 
    playlist_id = re.search(r"list=([a-zA-Z0-9_-]+)", playlist_url) 
    if not playlist_id:
        print(f"Error: Can't get playlist ID from URL: {playlist_url}")
        return []
    playlist_id = playlist_id.group(1)

    youtube = build('youtube', 'v3', developerKey=api_key)

    videos_info = []
    next_page_token = None

    try:
        while True:
            request = youtube.playlistItems().list(
                part="snippet",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute() # 

            # 
            for item in response.get('items', []):
                if item and 'snippet' in item:
                    video_id = item['snippet']['resourceId'].get('videoId')
                    video_title = item['snippet'].get('title')
                    if video_id and video_title:
                        videos_info.append({
                            "title": clean_string_keep_cyrillic_alphanumeric_and_space(video_title),
                            "url": f"https://www.youtube.com/watch?v={video_id}"
                        })

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break 

        return videos_info

    except HttpError as e:
        print(f"Error while accessing YouTube Data API: {e}")
        if e.resp.status == 400:
            print("Check plaulist ID or URL")
        elif e.resp.status == 403:
            print("Check your API key and its quota")
        elif e.resp.status == 404:
            print("Playlist not found or it is private")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

# Get subtitles from one youtube video and return it as text 
def get_youtube_captions_from_one_video(video_url: str, lang_codes: list = ['uk', 'ru','en', 'es', 'fr', 'de', 'he' ,'it' , 'pl' ,'pt' ,'tr', 'az', 'cs', 'ar', 'zh']):
    # Validate and extract ID of the video
    video_id = None
    if 'v=' in video_url:
        video_id = video_url.split('v=')[-1].split('&')[0]
    elif 'youtu.be/' in video_url:
        video_id = video_url.split('youtu.be/')[-1].split('?')[0]

    if not video_id:
        print(f"Error: Impossible to get video ID from URL: {video_url}")
        return None

    # Get subtitles from video 
    #print(f"Info: Attempt to load subtitles for ID: {video_id}")
    try:
        if lang_codes:
            # 
            transcript = YouTubeTranscriptApi.list_transcripts(video_id).find_transcript(lang_codes)
            transcript_data = transcript.fetch()
            lang_code = transcript.language_code
        else:
            # 
            transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
            lang_code = 'undefined'
                    
        if transcript_data is not None:
            full_text = " ".join([getattr(segment, 'text', '') for segment in transcript_data])
            cleaned_text = clean_string_keep_cyrillic_alphanumeric_and_space(full_text)
            return cleaned_text
        else:
            pass
            #print("Subtitles are not got")

    except NoTranscriptFound:
        print(f"Error: captions wasn't found for video '{video_url}'")
        print("It is possible that this video doesn't have captions")
    except TranscriptsDisabled:
        print(f"Error: Captions are switched off for this video '{video_url}'.")
    except Exception as e:
        print(f"Error: An unexpected error occurred while getting captions for video '{video_url}': {e}")

    return None

def get_captions(video_url_list):
    ''' Get captions from youtube.
    It proceed with url of video(s) and playlist(s) as well placed within input list

    returns list of dictionaries with format
        
    '''
    list_of_playlist_to_save = []
    # Define 
    for video_url in video_url_list:
        #Check if it is playlist
        if 'list=' in video_url:
            #get list of videos in that playlist using google api
            playlist_videos = get_youtube_playlist(video_url)
            #Check if the playlist has any video
            if playlist_videos:
                print(f"Found {len(playlist_videos)} video(s) in playlist")
                for video in playlist_videos:
                    caption_text = get_youtube_captions_from_one_video(video['url'])
                    caption_text = caption_text if caption_text else ""
                    video['captions'] = caption_text
                    if caption_text:
                        list_of_playlist_to_save.append(video)
                        print(f"Title: {video['title']}\nURL: {video['url']}\nCaptions: {video['captions'][:100]}\n------------")
            else:
                print("Error")
        else:
            #it is single video
            #get captions from one video
            caption_text = get_youtube_captions_from_one_video(video_url)
            caption_text = caption_text if caption_text else ""
            if caption_text:
                video_title = get_youtube_video_title(video_url)
                video_title = video_title if video_title else "No title"
                video = {'title': video_title, 'url': video_url, 'captions': caption_text}
                list_of_playlist_to_save.append(video)
                print(f"Title: {video['title']}\nURL: {video['url']}\nCaptions: {video['captions'][:100]}\n------------")


    
    save_youtube_captions_to_file(list_of_playlist_to_save)

    return 


if __name__ == "__main__":
    # Example usage
    test_playlist_url = "https://www.youtube.com/playlist?list=PL4sbV49yxRUhtG1BxSqD-PrnUBbXB2_06"
    test_video_url1 = "https://www.youtube.com/watch?v=xLfTcVkD3CU&t=182s"
    test_video_url2 = "https://www.youtube.com/watch?v=_IGFnG_czMk"

    test_video_url_list = [ test_video_url1, test_video_url2]

    print("Info: Start getting captions from youtube")
    get_captions(test_video_url_list)
    print("Info: End getting captions from youtube")
    

