import cv2
import numpy as np
import requests
import json
import argparse

# Define the command line arguments
ap = argparse.ArgumentParser()
ap.add_argument("-b", "--brand", type=str, required=True, help="The brand of the security camera being used")
args = vars(ap.parse_args())

# Check which brand of camera the user selected
if args['brand'].lower() == 'annke':
    # Connect to the Annke security camera
    cap = cv2.VideoCapture(0)

elif args['brand'].lower() == 'hikvision':
    # Connect to the Hikvision security camera
    cap = cv2.VideoCapture(1)

elif args['brand'].lower() == 'dahua':
    # Connect to the Dahua security camera
    cap = cv2.VideoCapture(2)

# Set the Clearview AI API endpoint and authentication token
clearview_api_endpoint = 'https://api.clearview.ai'
clearview_auth_token = 'YOUR_CLEARVIEW_AUTH_TOKEN'

# Define the parameters for the Clearview AI API request
headers = {'User-Agent': 'Mozilla/5.0', 'Authorization': 'Token ' + clearview_auth_token}
params = {'image': '', 'subject_id': '', 'gallery_name': ''}

# Define the URL of the camera stream
camera_url = 'YOUR_CAMERA_STREAM_URL'

# Open the camera stream
cap = cv2.VideoCapture(camera_url)

# Check if the camera stream was successfully opened
if not cap.isOpened():
    print('Unable to open camera stream')
    exit()

# Loop through the camera stream frames
while True:
    # Read the next frame from the camera stream
    ret, frame = cap.read()

    # Check if the frame was successfully read
    if not ret:
        print('Unable to read frame')
        break

    # Convert the frame to a JPEG image
    _, img_encoded = cv2.imencode('.jpg', frame)
    img_bytes = img_encoded.tobytes()

    # Set the Clearview AI API request parameters
    params['image'] = img_bytes
    params['subject_id'] = 'security_camera'
    params['gallery_name'] = 'security_cameras'

    # Send the image to the Clearview AI API for facial recognition
    response = requests.post(clearview_api_endpoint + '/face/match', headers=headers, params=params)

    # Check if the API request was successful
    if response.status_code != 200:
        print('Clearview AI API request failed')
        break

    # Parse the API response to get the recognized faces
    recognized_faces = json.loads(response.text)

    # Draw bounding boxes around the recognized faces
    for face in recognized_faces:
        box = face['box']
        cv2.rectangle(frame, (box['left'], box['top']), (box['right'], box['bottom']), (0, 255, 0), 2)

    # Display the frame with recognized faces
    cv2.imshow('Security Camera', frame)

    # Wait for the user to press a key
    if cv2.waitKey(1) == ord('q'):
        break

# Release the camera stream and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()
