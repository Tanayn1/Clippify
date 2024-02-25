import assemblyai as aai 
import os
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
import pysrt
import cv2
import numpy as np






from dotenv import load_dotenv


load_dotenv()
ASSEMBLY_API_KEY = os.getenv("ASSEMBLY_API_KEY")

aai.settings.api_key = f"{ASSEMBLY_API_KEY}"

def time_to_seconds(time_obj):
    return time_obj.hours * 3600 + time_obj.minutes * 60 + time_obj.seconds + time_obj.milliseconds / 1000



def create_subtitle_clips(subtitles, videosize,fontsize=36, font='Arial-bold', color='White', debug = False):
    subtitle_clips = []

    for subtitle in subtitles:
        start_time = time_to_seconds(subtitle.start)
        end_time = time_to_seconds(subtitle.end)
        duration = end_time - start_time

        video_width, video_height = videosize
        
        text_clip = TextClip(subtitle.text.upper(), fontsize=fontsize, font=font, color=color, transparent=True ,size=(video_width*3/4, None), method='caption').set_start(start_time).set_duration(duration)
        subtitle_x_position = 'center'
        subtitle_y_position = video_height* 3 / 5 

        text_position = (subtitle_x_position, subtitle_y_position)                    
        subtitle_clips.append(text_clip.set_position(text_position))

    return subtitle_clips


def loadSubtitles(video_path, output, srtOutput):
   transcriber = aai.Transcriber()
   transcript = transcriber.transcribe(video_path)

   srtSubtitles = transcript.export_subtitles_srt()

   with open(srtOutput, 'w') as f:
      f.write(srtSubtitles)


      
   video = VideoFileClip(video_path)
   subtitles = pysrt.open(srtOutput)

   subtitle_clips = create_subtitle_clips(subtitles,video.size)
   final_video = CompositeVideoClip([video] + subtitle_clips)
   final_video.write_videofile(output)
   os.remove(srtOutput)

   




  
   







