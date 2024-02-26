import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

CREATOMATE_API_KEY=os.getenv('CREATOMATE_API_KEY')


def generateSubtitles(videolink): 
    options = {
    # The ID of the template that you created in the template editor
    'template_id': '7cc08984-77d3-40f4-92d3-00de91680045',

    # Modifications that you want to apply to the template
    'modifications': {
    
        'Video-1': "https://clippifyvidsdemo.s3.ap-southeast-2.amazonaws.com/clip2.mp4",
    },
    }

    response = requests.post(
    'https://api.creatomate.com/v1/renders',
    headers={
        'Authorization': f'Bearer {CREATOMATE_API_KEY}',
        'Content-Type': 'application/json',
    },
    json=options
    )

    print(response.content)
    parsedResponse = json.loads(response.content)



    return parsedResponse