import cv2

# Replace the below URL with your ESP32-CAM video stream URL
stream_url = 'http://192.168.0.130:81/stream'

# Create a VideoCapture object
cap = cv2.VideoCapture(stream_url)

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Check if frame is not empty
    if not ret:
        continue

    # Display the resulting frame
    cv2.imshow('frame', frame)

    # Press Q on keyboard to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
