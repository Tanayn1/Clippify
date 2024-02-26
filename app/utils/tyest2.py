import json
response_data = b'[{"id":"7be72234-eec7-40c6-b98a-f899ce067eb0","status":"planned","url":"https://cdn.creatomate.com/renders/7be72234-eec7-40c6-b98a-f899ce067eb0.mp4","snapshot_url":"https://cdn.creatomate.com/snapshots/7be72234-eec7-40c6-b98a-f899ce067eb0.jpg","template_id":"7cc08984-77d3-40f4-92d3-00de91680045","template_name":"Compact Subtitles","template_tags":[],"output_format":"mp4","modifications":{"Video-1":"https://clippifyvidsdemo.s3.ap-southeast-2.amazonaws.com/clip2.mp4"}}]'

json_data = json.loads(response_data)

# Extract URL from the first object in the array
url = json_data[0]['url']

print("URL:", url)