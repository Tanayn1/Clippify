import requests



def getTimestamps(transcript, audio) :
    # Define the URL of the Gentle API
    gentle_url = 'http://localhost:32768/transcriptions?async=false'

    # Define the path to the audio file and transcript file
    audio_file = audio
    

    # Create a dictionary containing the audio and transcript files
    files = {
        'audio': open(audio_file, 'rb'),
        'transcript': transcript
    }

    # Make a POST request to the Gentle API
    response = requests.post(gentle_url, files=files)

    # Check if the request was successful
    if response.status_code == 200:
        # Print the transcription result
        #print(response.json())
        timestamps = response.json()

        firstword = timestamps['words'][0]['start']
        lastword = timestamps['words'][-1]['end']
     
        print(firstword, lastword)

        return firstword, lastword
    else:
        # Print an error message
        print('Error:', response.status_code)



