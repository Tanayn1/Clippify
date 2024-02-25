import cv2
from moviepy.editor import VideoFileClip, ImageSequenceClip
import numpy as np

def detect_faces(input_file):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(input_file)

    faces = []

    while len(faces) < 5:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        detected_faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for face in detected_faces:
            if not any(np.array_equal(face, f) for f in faces):
                faces.append(frame[face[1]:face[1] + face[3], face[0]:face[0] + face[2]])

        print(f"Number of unique faces detected: {len(faces)}")

    cap.release()
    cv2.destroyAllWindows()

    return faces

'''
def resize_video_centered(input_file, output_file, faces):
    # Calculate the aspect ratio
    aspect_ratio = 9 / 16

    # Calculate the new width and height
    width = int(1080 * aspect_ratio)
    height = 1080

    # Create a new video clip with the desired aspect ratio
    video = VideoFileClip(input_file)

    # Resize the entire frame instead of just the face region
    resized_video = video.resize((width, height))

    # Extract duration of each frame in the original video
    frame_durations = 1 / video.fps

    # Create a new video clip using the resized frame and durations
    if faces:
        new_video = ImageSequenceClip([resized_video.get_frame(i / video.fps) for i in range(int(video.duration * video.fps))], fps=video.fps, durations=[frame_durations] * int(video.duration * video.fps))
    else:
        new_video = resized_video

    # Write the new video to the output file
    new_video.write_videofile(output_file)
'''
def resize_video_centered(input_file, output_file, faces):
    # Calculate the aspect ratio
    aspect_ratio = 9 / 16

    # Calculate the new width and height
    width = int(1080 * aspect_ratio)
    height = 1080

    # Create a new video clip with the desired aspect ratio
    video = VideoFileClip(input_file)

    # Filter out faces with invalid shapes
    valid_faces = [face for face in faces if len(face) == 4]

    # Calculate the center of the face bounding boxes
    if valid_faces:
        avg_face_x = sum((face[0] + face[2]) / 2 for face in valid_faces) / len(valid_faces)
        avg_face_y = sum((face[1] + face[3]) / 2 for face in valid_faces) / len(valid_faces)
    else:
        # If no valid faces are detected, use the center of the frame
        avg_face_x = video.size[0] / 2
        avg_face_y = video.size[1] / 2

    print("Average face position:", avg_face_x, avg_face_y)

    # Calculate the cropping coordinates
    crop_x1 = max(0, int(avg_face_x - width / 2))
    crop_y1 = max(0, int(avg_face_y - height / 2))
    crop_x2 = min(video.size[0], crop_x1 + width)
    crop_y2 = min(video.size[1], crop_y1 + height)

    print("Cropping coordinates:", crop_x1, crop_y1, crop_x2, crop_y2)

    # Crop the video
    cropped_video = video.crop(x1=crop_x1, y1=crop_y1, x2=crop_x2, y2=crop_y2)

    # Extract duration of each frame in the original video
    frame_durations = 1 / video.fps

    # Create a new video clip using the cropped frame and durations
    if valid_faces:
        new_video = ImageSequenceClip([cropped_video.get_frame(i / video.fps) for i in range(int(video.duration * video.fps))], fps=video.fps, durations=[frame_durations] * int(video.duration * video.fps))
    else:
        new_video = cropped_video

    # Write the new video to the output file with the codec parameter specified
    new_video.write_videofile(output_file, codec='libx264')

    return output_file

    





