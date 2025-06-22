#from pytube import YouTube
from moviepy import VideoFileClip, Clip 
from pathlib import Path

def cut_video(input_file, output_file, start_time, end_time):
    with VideoFileClip(input_file, audio=False).subclipped(start_time, end_time) as clip:
        clip.write_videofile(output_file, audio=False, codec="libx264")


if __name__ == "__main__":
   
   current_script_dir = Path(__file__).parent
   file_input_path = current_script_dir / "video" / "input_video" / "videoplayback1.mp4"
   file_output_path = current_script_dir / "video" / "output_video" / "videoplayback1.mp4"
   file_temp_path = current_script_dir / "video" / "output_video" / "temp.mp4"

   #if file_input_path.exists() and file_input_path.is_file():
   #     cut_video(str(file_input_path), str(file_output_path), 20, 30)



    

