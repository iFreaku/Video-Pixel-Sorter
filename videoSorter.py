import cv2 # pip install opencv-python
import numpy as np # pip install numpy
import os
import random
import subprocess

# Extracts each frame of the video and saves them in a folder
def extractFrames(input_video, output_folder):
    cap = cv2.VideoCapture(input_video)
    frame_count = 0

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    fps = int(cap.get(cv2.CAP_PROP_FPS))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.png")
        cv2.imwrite(frame_filename, frame)

    cap.release()
    cv2.destroyAllWindows()

    return frame_count, fps

# Sorts the pixel of each image and saves them in sortedFolder
def sortPixels(input_folder, output_folder):
    files = os.listdir(input_folder)
    files.sort()

    for filename in files:
        if filename.endswith(".png"):
            img = cv2.imread(os.path.join(input_folder, filename))
            sorted_img = np.sort(img, axis=0)
            sorted_filename = os.path.join(output_folder, filename)
            cv2.imwrite(sorted_filename, sorted_img)

# Takes all the images from the sortedFolder and makes a video of it using ffmpeg
def createVideo(input_folder, output_video, frame_count, fps):
    ffmpeg_command = [
        "ffmpeg",
        "-framerate", str(fps),
        "-i", os.path.join(input_folder, "frame_%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        output_video
    ]

    try:
        subprocess.run(ffmpeg_command, check=True)
        print("Video creation completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating the video: {e}")

# Cleaning up the images :)
def clean(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

# Main
if __name__ == "__main__":

    outputFolder = r"\extractedFramesFolder"
    sortedFolder = r"\sorted_frames"
    inputVideo = r"inputVideo.mp4"
    outputVideo = f"output_video.mp4"
    

    frame_count, fps = extractFrames(inputVideo, outputFolder)
    sortPixels(outputFolder, sortedFolder)
    createVideo(sortedFolder, outputVideo, frame_count, fps)

    clean(outputFolder)
    clean(sortedFolder)

    print("Video processing completed!")
    os.startfile(outputVideo)
