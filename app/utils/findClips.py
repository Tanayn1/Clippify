from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

API_KEY = os.getenv("OPEN_AI_KEY")

client = OpenAI(
    api_key= API_KEY,
)

def getClips(transcription) :
    try :
        response = client.chat.completions.create(
        model="ft:gpt-3.5-turbo-1106:personal::8sMt2QBq",
        messages= [
            {"role": "system", "content": "You are an AI that extracts the most viral tiktoks/shorts from long form content."},
            {"role": "user", "content": f"Get the most viral tiktok/shorts clips from the transcript provided. Provide A title with each clip in JSON format. Here is the Transcript: {transcription}"}
        ])

        

        content = response.choices[0].message.content

        jsonContent = json.loads(content)

        

        clips = []

        for clipTitle, clipTranscription in jsonContent.items():
         clips_dict = {
            'title' : clipTitle,
            'transcript': clipTranscription
         }
         clips.append(clipTranscription)
        
        
        print(clips)
     


        return clips

    except Exception as e :
     print("error", e)
     return None
    




