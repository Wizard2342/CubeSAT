import time
import board

from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
from git import Repo
import time
import bluepy3
from picamera2 import Picamera2, Preview
from libcamera import ColorSpace
import imgproc
import cv2
import numpy as np
import time
import os
from google.colab.patches import cv2_imshow

picam2 = Picamera2()
preview_config = picam2.create_preview_configuration(main = {'size':(800,600)})
picam2.configure(preview_config)

picam2.start_preview(Preview.QTGL)
picam2.start()

time.sleep(2)

#VARIABLES
THRESHOLD = 0      #Any desired value from the accelerometer
REPO_PATH = "/home/cube/CubeSAT"     #Your github repo path: ex. /home/pi/FlatSatChallenge
FOLDER_PATH = "Pictures"   #Your image folder path in your GitHub repo: ex. /Images

#imu and camera initialization
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)

def img_gen(name):
    t = time.strftime("_%H%M%S")
    imgname = (f'{REPO_PATH}/{FOLDER_PATH}/{name}{t}.jpg')

    print(imgname)
    return imgname

def take_photo():
    print(accelx)
    name='greatname'
    time.sleep(1)
    metadata = picam2.capture_file(str(img_gen('great')))
    V4L2_HSV_ENC_256
    print(metadata)
    picam2.close()

def convert_to_8bit_grayscale(img, index):
    # Read the image
    image = cv2.imread(img)

    # Convert the image to grayscale
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Convert the grayscale image to 8-bit
    eight_bit_image = cv2.convertScaleAbs(grayscale_image)

    # Generate a unique filename based on timestamp with milliseconds and index
    timestamp = time.strftime("%Y%m%d_%H%M%S_%f")
    filename = f"grayscale_image_{index}_{timestamp}.jpg"

    # Save the grayscale image
    cv2.imwrite(filename, eight_bit_image)

    return filename

def delete_old_pictures(folder_path):
    # Get a list of all files in the folder
    files = os.listdir(folder_path)

    # Filter out non-image files
    image_files = [f for f in files if f.endswith('.jpg')]

    # Sort the image files based on modification time
    image_files.sort(key=lambda x: os.path.getmtime(os.path.join(folder_path, x)))

    # Keep the latest and second latest images, delete the rest
    images_to_keep = image_files[-2:]

    if images_to_keep:  # Check if the list is not empty
        for file_name in image_files[:-2]:
            file_path = os.path.join(folder_path, file_name)
            os.remove(file_path)
            print(f"Deleted: {file_path}")

        # Output the file paths of the latest and second latest images
        image1_path = os.path.join(folder_path, images_to_keep[-1])
        image2_path = os.path.join(folder_path, images_to_keep[-2])
        return image1_path, image2_path
    else:
        print("No image files found in the folder.")
        return None, None
while True:
    # Get the paths of the latest and second latest images
    latest_image_path, second_latest_image_path = delete_old_pictures(FOLDER_PATH)

    if latest_image_path and second_latest_image_path:  # Check if paths are valid
        # Convert images to grayscale and save them
        grayscale_image1_path = convert_to_8bit_grayscale(latest_image_path, 1)
        grayscale_image2_path = convert_to_8bit_grayscale(second_latest_image_path, 2)
    time.sleep(120)
