import json
import segmentvideo
import cropvideo2
from dotenv import load_dotenv
import os
import subtitles
from moviepy.editor import VideoFileClip
import boto3
load_dotenv()


AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

s3 = boto3.resource(
    service_name = 's3',
    region_name= 'ap-southeast-2',
    aws_access_key_id = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
)


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
    formmatedVideoName = video_name.replace(" ", "")
    
    
    croppedClip =  cropvideo2.resize_video_centered(clip, formmatedVideoName, faces)
    s3.meta.client.upload_file(croppedClip, 'clippifyvidsdemo', formmatedVideoName)
    objecturl = f"https://clippifyvidsdemo.s3.ap-southeast-2.amazonaws.com/{croppedClip}"
    finishedClips.append(objecturl)
   
    


print(finishedClips)    
