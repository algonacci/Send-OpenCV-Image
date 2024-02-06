from flask import Flask, request, Response, jsonify
import numpy as np
import imageio
import cv2

app = Flask(__name__)

# Create a dictionary to store frames for different cameras
camera_frames = {}


@app.route('/upload/<camera_id>', methods=['POST'])
def upload(camera_id):
    # Get the image data from the POST request
    image_data = request.files['image'].read()

    # Convert the image data to a NumPy array
    nparr = np.frombuffer(image_data, np.uint8)

    # Decode the image array using OpenCV
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Check if the camera_id exists in the dictionary, and create a list for frames if not
    if camera_id not in camera_frames:
        camera_frames[camera_id] = []

    # Append the frame to the list of frames for the specific camera
    camera_frames[camera_id].append(frame)
    print(camera_frames)

    return jsonify({'message': f'Frame received and added to camera {camera_id}.'})


@app.route('/compile/<camera_id>', methods=['GET'])
def compile_video(camera_id):
    if camera_id not in camera_frames or not camera_frames[camera_id]:
        return jsonify({'message': f'No frames for camera {camera_id} to compile.'})

    output_video_file = f"output_video_{camera_id}.mp4"
    output_video = imageio.get_writer(
        output_video_file, fps=30, macro_block_size=1)

    for frame in camera_frames[camera_id]:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output_video.append_data(frame)

    output_video.close()
    del camera_frames[camera_id]  # Remove frames after compilation

    return jsonify({'message': f'Video for camera {camera_id} compiled successfully.'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
