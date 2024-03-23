"""
The Python code you will write for this module should read
acceleration data from the IMU. When a reading comes in that surpasses
an acceleration threshold (indicating a shake), your Pi should pause,
trigger the camera to take a picture, then save the image with a
descriptive filename. You may use GitHub to upload your images automatically,
but for this activity it is not required.

The provided functions are only for reference, you do not need to use them. 
You will need to complete the take_photo() function and configure the VARIABLES section
"""

#AUTHOR: Srivathsa Raj
#DATE: 3/22/2024

#import libraries
import time
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
#from git import Repo
import time
import bluepy3
from libcamera import ColorSpace
import imgproc
from picamera2 import Picamera2, Preview
import cv2

picam2 = Picamera2()
preview_config = picam2.create_preview_configuration(main = {'size':(800,600)})
picam2.configure(preview_config)

picam2.start_preview(Preview.QTGL)

picam2.start()

time.sleep(2)



#VARIABLES
THRESHOLD = 0      #Any desired value from the accelerometer
REPO_PATH = "/home/cube/CubeSAT"     #Your github repo path: ex. /home/pi/FlatSatChallenge
FOLDER_PATH = "pictures"   #Your image folder path in your GitHub repo: ex. /Images

#imu and camera initialization
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)

#def pi_restart(type):
	#We need to restart the Raspberry Pi and alert ground station
	#pi_restart=1 means IMU failed
	#pi_restart=0 means Camera failed


def camera_init():
	i2c = board.I2C()
	metadata = picam2.capture_file(str(img_gen('ggreat')))
	if metadata is None:
		pi_restart(0)
		
		
def imu_init()
	accel_gyro = LSM6DS(i2c)
	mag = LIS3MDL(i2c)
	accelx, accely, accelz = accel_gyro.acceleration
	if accelx or accely or accelz is None:
		pi_restart(1)
	else:
		print("Working")



#def bluetooth_init()
	#Write bluepy3-specific code	


def img_gen(name):

    """
    This function is complete. Generates a new image name.

    Parameters:
        name (str): your name ex. MasonM
    """
    t = time.strftime("_%H%M%S")
    imgname = (f'{REPO_PATH}/{FOLDER_PATH}/{name}{t}.jpg')
    print(imgname)
    return imgname


def take_photo():
	print(accelx)
	name='greatname'
	time.sleep(1)
	metadata = picam2.capture_file(str(img_gen('great)))
	#V4L2_HSV_ENC_256
	print(metadata)
	picam2.close()


def convert_to_8bit_grayscale(img):
    # Read the image
    image = cv2.imread(img)

    # Convert the image to grayscale
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Convert the grayscale image to 8-bit
    eight_bit_image = cv2.convertScaleAbs(grayscale_image)

    return eight_bit_image
	


def ImgChangeAnalysis():
	num_horizontal_divisions = 20
	num_vertical_divisions = 56
	hor_pixel_val = 164
	ver_pixel_val = 44

	batch_list = []

	for x in range (num_horizontal_divisons):
		for y in range(num_vertical_divisions):
			x_coor = x * hor_pixel_val
			x_coor = x * 

	#1. divide the batches, number the batches, put it into a list/index

def main():
    take_photo()


if __name__ == '__main__':
    main()