from typing import Union
from app.utils import transcribe, findClips, getTimestamps, segmentvideo, cropvideo2, creaotomateSubtitles
from fastapi import FastAPI
from pydantic import BaseModel
import os
import boto3

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

s3 = boto3.resource(
    service_name = 's3',
    region_name= 'ap-southeast-2',
    aws_access_key_id = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
)

app = FastAPI()

class clipRequest(BaseModel):
 ytUrl: str


@app.post("/clippify")

def clippify(request: clipRequest):
 try:
    transcript = transcribe.getTranscription(request.ytUrl)
    clipsShortTranscripts = findClips.getClips(transcript)
    print(clipsShortTranscripts)
    timestamps = []
    titles = []
    output = 'audio'
    audio = transcribe.download_audio_from_youtube(request.ytUrl, output)
    for i in range(len(clipsShortTranscripts)):
     transcripts = clipsShortTranscripts[i]['transcript']
     title = clipsShortTranscripts[i]['title']
     firstword, lastword = getTimestamps.getTimestamps(transcripts, audio)
     my_tuple = (firstword, lastword)
     timestamps.append(my_tuple)
     titles.append(title)


    output_folder = 'output'
    clips = segmentvideo.clip_video_with_timestamps(request.ytUrl, timestamps, output_folder) 

    finishedClips = []
    

    for i, title in enumerate(titles) :
     clip = clips[i]
     faces = cropvideo2.detect_faces(clip)
     clip_name= f"{titles[i]}.mp4"
     formmatedClipName = clip_name.replace(" ", "")
     croppedClip = cropvideo2.resize_video_centered(clip, formmatedClipName, faces)
     s3.meta.client.upload_file(croppedClip, 'clippifyvidsdemo', formmatedClipName)
     objecturl = f"https://clippifyvidsdemo.s3.ap-southeast-2.amazonaws.com/{croppedClip}"
     response = creaotomateSubtitles.generateSubtitles(objecturl)
     finishedClips.append(response[0]['url'])
   
     
     
    


    print('success', finishedClips) 
    
    return finishedClips
    
 except Exception as e: 
  print(e)
 