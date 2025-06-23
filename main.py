import split_video_opencv
from pathlib import Path
import time
import datetime    
    
if __name__ == "__main__":
    
    

    #Trim video for smaller dslices without cropping
    start_time = time.time()
    
    current_script_dir = Path("C:/")
    file_input_path_trim = str(current_script_dir / "video" / "input_video" / "video_2025-06-23_07-42-40.mp4")
    start = 0
    video_length = 8
    for i in range(10):
        start_time_trim = time.time()
        print(f"Video processing: {i + 1}/10")
        file_name= 'video '+datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")+'.mp4'
        file_output_path_trim = str(current_script_dir / "video" / "output_video" / file_name)
        success_trim = split_video_opencv.trim_video_opencv(file_input_path_trim, file_output_path_trim, start, video_length)
        start += video_length
        if success_trim:
            print(f"Success: Trim duration: {time.time() - start_time_trim:.4f} sec.")
        else:
            print("Error trim")
    



