from youtube_transcript_api._api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled
from common_func import clean_string_keep_cyrillic_alphanumeric_and_space

# Get subtitles from one youtube video and return it as text 
def get_youtube_subtitles(video_url: str, lang_codes: list = []):
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
            #print("Subtitles are not gotten")

    except NoTranscriptFound:
        print(f"Error: subtitels wasn't found for video '{video_id}'")
        print("It is possible that this video doesn't have subtitles")
    except TranscriptsDisabled:
        print(f"Error: Subtitles are switched off for this video '{video_id}'.")
    except Exception as e:
        print(f"Error: An unexpected error occurred while getting subtitles for video '{video_id}': {e}")

    return None

"""def get_youtube_playlist1(playlist_url:str)
    # Validate and extract ID of the playlist 
    # #AIzaSyBWgU_1YFk9DzLLk0A_ooV_YFRjutGbCXk
    playlist_id = None
    if 'list=' in playlist_url:
        playlist_id = playlist_url.split('list=')[-1].split('&')[0]
    else:
        print(f"Error: Impossible to get playlist ID from URL: {playlist_url}")
        return None

    # Get subtitles from video
    print(f"Info: Attempt to load subtitles for ID: {playlist_id}")
 """   



if __name__ == "__main__":
    # Example usage
    video_url = "https://www.youtube.com/watch?v=FezVkh_VSzM" 
    subtitles_text = get_youtube_subtitles(video_url, lang_codes=['ru', 'uk', 'en', 'a.en', 'uk', 'a.uk']) 
    subtitles_text = subtitles_text if subtitles_text else ""
    print(subtitles_text[:500] + "...") 



   

