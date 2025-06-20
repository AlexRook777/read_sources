from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from common_func import clean_string_keep_cyrillic_alphanumeric_and_space
import re

def get_youtube_playlist(playlist_url: str, api_key='AIzaSyBWgU_1YFk9DzLLk0A_ooV_YFRjutGbCXk'):
    ''' 
    Get list of video from youtube playlist
    
    Input: 
        - playlist_url - textt stribg with full url to playlist
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
                            "id": video_id,
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



#------------------
if __name__ == "__main__":
    api_key = "AIzaSyBWgU_1YFk9DzLLk0A_ooV_YFRjutGbCXk" 
    test_playlist_url = "https://www.youtube.com/playlist?list=PL4sbV49yxRUhtG1BxSqD-PrnUBbXB2_06"

    playlist_videos = get_youtube_playlist(test_playlist_url, api_key)
    if playlist_videos:
        print(f"Found {len(playlist_videos)} video(s) in playlist")
        #print(playlist_videos)
        for video in playlist_videos: 
            print(f"Title: {video['title']}\n      ID: {video['id']}\n      URL: {video['url']}")
    else:
        print("Error")

 
