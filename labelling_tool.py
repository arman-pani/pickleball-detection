import argparse
import os
import sys

import cv2
from utils import go2frame, load_info, save_info, show_image

# Argument Parser
parser = argparse.ArgumentParser()
parser.add_argument('--label_video_path', type=str, required=True, help='Path to the video file for labeling')
parser.add_argument('--csv_path', type=str, required=True, help='Path to the CSV file containing labeled data')
args = parser.parse_args()

# Validate video path
video_path = args.label_video_path
if not os.path.isfile(video_path) or not video_path.endswith('.mp4'):
    print("Invalid video path! Please provide a valid .mp4 file.")
    sys.exit(1)

# Validate CSV path
csv_path = args.csv_path
load_csv = os.path.isfile(csv_path) and csv_path.endswith('.csv')
if not load_csv:
    print("Invalid CSV file! A new label file will be created.")

# Open video capture
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error: Could not open video file.")
    sys.exit(1)

fps = int(cap.get(cv2.CAP_PROP_FPS))
n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Load or create labeling data
data = load_info(csv_path) if load_csv else {}
if not load_csv or len(data) != n_frames:
    print("Creating a new label dictionary.")
    data = {idx: {'Frame': idx, 'Ball': 0, 'x': -1, 'y': -1} for idx in range(n_frames)}
else:
    print("Loaded labeled data successfully.")

# Mouse callback function for labeling
def ball_label(event, x, y, flags, param):
    global frame_no, data, frame
    if event == cv2.EVENT_LBUTTONDOWN:
        h, w, _ = frame.shape
        data[frame_no]['x'] = x / w
        data[frame_no]['y'] = y / h
        data[frame_no]['Ball'] = 1
    elif event == cv2.EVENT_MBUTTONDOWN:
        data[frame_no]['x'] = -1
        data[frame_no]['y'] = -1
        data[frame_no]['Ball'] = 0

# Initialize display
frame_no = 0
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
ret, frame = cap.read()
if not ret:
    print("Error: Could not read the first frame.")
    sys.exit(1)

cv2.namedWindow('Frame Labeling', cv2.WINDOW_NORMAL)  # Allows resizing
cv2.resizeWindow('Frame Labeling', min(frame_width, 1280), min(frame_height, 720))
cv2.setMouseCallback('Frame Labeling', ball_label)
show_image(frame, frame_no, data[frame_no]['x'], data[frame_no]['y'])

# Keyboard interaction loop
while True:
    cv2.imshow('Frame Labeling', frame)
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('e'):
        print("Exiting program.")
        cap.release()
        cv2.destroyAllWindows()
        sys.exit(0)
    elif key == ord('s'):
        save_info(data, csv_path)
        print("Labels saved successfully.")
    elif key == ord('n') and frame_no < n_frames - 1:
        frame_no += 1
    elif key == ord('p') and frame_no > 0:
        frame_no -= 1
    elif key == ord('f'):
        frame_no = 0
    elif key == ord('l'):
        frame_no = n_frames - 1
    elif key == ord('>'):
        frame_no = min(frame_no + 36, n_frames - 1)
    elif key == ord('<'):
        frame_no = max(frame_no - 36, 0)
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
    ret, frame = cap.read()
    if not ret:
        print(f"Error: Could not read frame {frame_no}")
        continue
    
    show_image(frame, frame_no, data[frame_no]['x'], data[frame_no]['y'])