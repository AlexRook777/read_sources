from youtube_transcript_api._api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled

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
    print(f"Info: Attempt to load subtitles for ID: {video_id}")
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
            print(f"Success: Subtitles got saccessfully. Lenght: {len(full_text)}  Lang: {lang_code}")
            return full_text
        else:
            print("Subtitles are not gotten")

    except NoTranscriptFound:
        print(f"Error: subtitels wasn't found for video '{video_id}'")
        print("It is possible that this video doesn't have subtitles")
    except TranscriptsDisabled:
        print(f"Error: Subtitles are switched off for this video '{video_id}'.")
    except Exception as e:
        print(f"Error: An unexpected error occurred while getting subtitles for video '{video_id}': {e}")

    return None


video_url = "https://www.youtube.com/watch?v=FezVkh_VSzM" 
subtitles_text = get_youtube_subtitles(video_url, lang_codes=['ru', 'uk', 'en', 'a.en', 'uk', 'a.uk']) 
subtitles_text = subtitles_text if subtitles_text else ""
print(subtitles_text[:500] + "...") 

video_url = "https://www.youtube.com/watch?v=V4I0DH4J6yo&list=PL4sbV49yxRUhtG1BxSqD-PrnUBbXB2_06&index=2&t=537s" 
subtitles_text = get_youtube_subtitles(video_url, lang_codes=['ru', 'uk', 'en', 'a.en', 'uk', 'a.uk']) 
subtitles_text = subtitles_text if subtitles_text else ""
print(subtitles_text[:500] + "...") 

