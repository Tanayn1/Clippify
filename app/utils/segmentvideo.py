import os
import sys
import pytube
from moviepy.editor import VideoFileClip

def download_video(url, output_path="/temp"):
    try:
        youtube = pytube.YouTube(url)
        video = youtube.streams.get_highest_resolution()

        os.makedirs(output_path, exist_ok=True)
        video.download(output_path)

        title = video.title.replace("/", "_")
        return os.path.join(output_path, video.default_filename), title
    except Exception as e:
        print(f"Error downloading video: {e}")
        sys.exit(1)

def clip_video_with_timestamps(url, timestamps, output_folder="output"):
    # Download the video
    video_file, title = download_video(url)

    # Clean the title for folder name
    cleaned_title = ''.join(c for c in title if c.isalnum() or c in [' ', '_'])
    clip_folder = os.path.join(output_folder, cleaned_title + "_clips")
    os.makedirs(clip_folder, exist_ok=True)

    # Initialize VideoFileClip object
    video_clip = VideoFileClip(video_file)

    # Initialize an empty list to store the clips
    clips = []

    for i, (start_sec, end_sec) in enumerate(timestamps, start=1):
        # Clip the video
        clip = video_clip.subclip(start_sec, end_sec)
        
        # Define clip filename
        clip_filename = f"clip_{i}.mp4"
        
        # Define clip filepath
        clip_filepath = os.path.join(clip_folder, clip_filename)
        
        # Write the clipped video to file
        clip.write_videofile(clip_filepath, codec="libx264")
        
        # Append filepath to clips list
        clips.append(clip_filepath)

    # Close the video clip object
    video_clip.close()

    # Remove the original video file
    os.remove(video_file)

    return clips



'''
# Example usage
url = "https://www.youtube.com/watch?v=HsKY0crGSWE"
timestamps = [(0, 20), (20, 40), (40, 100)]  # Each tuple contains start and end seconds
output_folder = "output"

clips = clip_video_with_timestamps(url, timestamps, output_folder)
print("Clips saved:", clips)
'''