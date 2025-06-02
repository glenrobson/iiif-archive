import cv2
import numpy as np

# Video settings
filename = 'tests/fixtures/assets/video.mp4'
fps = 24
duration_seconds = 3
frame_width, frame_height = 640, 480

# Define the codec for MP4
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'avc1' on some systems if needed
out = cv2.VideoWriter(filename, fourcc, fps, (frame_width, frame_height))

# Generate frames
for i in range(fps * duration_seconds):
    color = (i % 256, (2 * i) % 256, (3 * i) % 256)  # RGB color changes
    frame = np.full((frame_height, frame_width, 3), color, dtype=np.uint8)
    out.write(frame)

out.release()
print(f"MP4 video saved as {filename}")
