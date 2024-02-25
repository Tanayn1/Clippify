from typing import Union
from app.utils import transcribe, findClips, getTimestamps, segmentvideo, cropvideo2, subtitles
from fastapi import FastAPI
from pydantic import BaseModel
import os



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
     croppedClip = cropvideo2.resize_video_centered(clip, clip_name, faces)
     srtOutput = f"{titles[i]}.srt"
     subtitle_clip_name= f"{titles[i]}subtiltled.mp4"
     finishedClip = subtitles.loadSubtitles(croppedClip, subtitle_clip_name, srtOutput)
     finishedClips.append(finishedClip)
     
     clip_url = f"/clips/{clip_name}"
     finishedClips.append(clip_url)
     
     
    


    print('success', finishedClips) 
    
    return finishedClips
    
 except Exception as e: 
  print(e)
 