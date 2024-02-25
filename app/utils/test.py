import json
import segmentvideo
import cropvideo2
from dotenv import load_dotenv
import os
load_dotenv()

API = os.getenv("OPEN_AI_KEY")

print(API)

'''
titles = ['clip1','clip2']

ytUrl = 'https://www.youtube.com/watch?v=moW2NDaymxg'
output_folder = 'output'

timestamps = [(10,20), (30, 40)]

clips = segmentvideo.clip_video_with_timestamps(ytUrl, timestamps, output_folder)

for i, title in enumerate(titles):
    clip = clips[i]
    faces = cropvideo2.detect_faces(clip)
    video_name = f"{title}.mp4"
    cropvideo2.resize_video_centered(clip, video_name, faces)
'''