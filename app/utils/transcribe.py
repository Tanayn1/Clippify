import assemblyai as aai
import os
from pytube import YouTube
import boto3

from dotenv import load_dotenv
load_dotenv()





ASSEMBLY_API_KEY = os.getenv("ASSEMBLY_API_KEY")

aai.settings.api_key = f"{ASSEMBLY_API_KEY}"

def download_audio_from_youtube(youtube_url, output_dir):
       try:
        # Create a YouTube object
        yt = YouTube(youtube_url)

        # Get the audio-only stream
        audio_stream = yt.streams.filter(only_audio=True).first()

        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Set the output filename to the title of the video
        title = yt.title.replace('/', '-')  # Replace invalid characters in the title
        output_filename = f"{title}.mp3"

        # Download the audio stream and save it with the specified filename
        audio_stream.download(output_dir, filename=output_filename)

        return os.path.join(output_dir, output_filename)

       except Exception as e:
        print(f"Error downloading audio: {e}")
        return None

    

    
def getTranscription(ytLink) :
        try :

            output_directory = 'audio'

            ytAudio = download_audio_from_youtube(ytLink, output_directory)

            config = aai.TranscriptionConfig(punctuate=False, format_text=False)

            transcriber = aai.Transcriber(config=config)

        # will use the same config for all `.transcribe*(...)` operations
            transcript = transcriber.transcribe(ytAudio)

            print(transcript.text)
            return transcript.text

        except Exception as e:
         print('Error', e)







