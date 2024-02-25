import json
import segmentvideo
import cropvideo2
from dotenv import load_dotenv
import os
import subtitles
from moviepy.editor import VideoFileClip
load_dotenv()



titles = ['clip1','clip2']

ytUrl = 'https://www.youtube.com/watch?v=moW2NDaymxg'
output_folder = 'output'

timestamps = [(10,20), (30, 40)]

clips = segmentvideo.clip_video_with_timestamps(ytUrl, timestamps, output_folder)

finishedClips= []


for i, title in enumerate(titles):
    clip = clips[i]
    faces = cropvideo2.detect_faces(clip)
    video_name = f"{title}.mp4"
    subtitle_VideoName = f"{title}subtiles.mp4"
    srtOutput = f"{title}.srt"
    croppedClip =  cropvideo2.resize_video_centered(clip, video_name, faces)
    finishedClip = subtitles.loadSubtitles(croppedClip, subtitle_VideoName, srtOutput)
    finishedClips.append(finishedClip)
    
    clip_url = f"/clips/{subtitle_VideoName}"
    finishedClips.append(clip_url)



print(finishedClips)    
