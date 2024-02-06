import cv2
import requests
import time

stream_url = 'http://192.168.0.130:81/stream'

# Create a VideoCapture object to access the camera (usually the default camera)
cap = cv2.VideoCapture(stream_url)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

frame_rate = 20  # Adjust the frame rate as needed
frame_interval = 1.0 / frame_rate
last_frame_time = time.time()

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame.")
        break

    # Display the frame in a window
    cv2.imshow('Camera Feed', frame)

    # Capture the current time
    current_time = time.time()

    # Calculate the time elapsed since the last frame
    elapsed_time = current_time - last_frame_time

    # Check if enough time has elapsed to send a frame
    if elapsed_time >= frame_interval:
        # Encode the image as JPEG
        _, encoded_image = cv2.imencode('.jpg', frame)

        # Convert the encoded image to bytes
        image_bytes = encoded_image.tobytes()

        # Send the image to the Flask server
        response = requests.post(
            'http://localhost:5000/upload/1', files={'image': ('image.jpg', image_bytes)})

        print(response.json())

        # Update the last frame time
        last_frame_time = current_time

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
