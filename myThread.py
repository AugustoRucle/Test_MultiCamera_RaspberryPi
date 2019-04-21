import cv2
import os
import time
import threading
import numpy as np
from time import sleep
from picamera import PiCamera

class Camera (threading.Thread):
    def __init__(self, name, times, path, camera):
        threading.Thread.__init__(self)
        self.name = name
        self.times = times
        self.path = path
        self.camera = camera

    def run(self):
        print ("Starting " + self.name)
        Init_Camera(self.path, self.times, self.camera)
        print ("Exiting " + self.name)

def Init_Camera(path, times, camera):

	path_img_1 = TakePicture(camera, path, "img_{}".format(0))	
	
	for i in range(1,10):
		#start time
		start_time = time.time()	
		
		path_img_2 = TakePicture(camera, path, "img_{}".format(i))
		print("Comparando: {} vs {}".format(path_img_1, path_img_2))
		ImageAligment(path_img_1, path_img_2)
		
		#Finish time
		finish_time = time.time()
		
		#Save difference of both times
		difference_times = finish_time - start_time
		times.append((difference_times, i))
		print("Duracion: {}".format(difference_times))
		
		path_img_1 = path_img_2

def TakePicture(camera, path, img_name, resolution = (640, 480)):
	
	if path == "PiCamera_img":
		return TakePicture_PiCamera(camera, path, img_name, resolution)
		
	elif path == "USBCamera_img":
		return TakePicture_USBCamera(camera, path, img_name, "-d /dev/video0")
	
	elif path == "USBCamera_img/camera0":
		return TakePicture_USBCamera(camera, path, img_name, "-d /dev/video0")
		
	elif path == "USBCamera_img/camera1":
		return TakePicture_USBCamera(camera, path, img_name, "-d /dev/video1")
		

def TakePicture_PiCamera(camera, path, img_name, resolution):
	
	#Full resolution = 2592, 1944
	
	#Create path
	path = '{}/{}.jpg'.format(path, img_name)	
	
	#Setting camera
	camera.rotation = 180
	camera.resolution = resolution
	
	# Camera warm-up time
	sleep(0.2)
	
	#Capture picture
	camera.capture(path)
	
	return path


def TakePicture_USBCamera(camera, path, img_name, device):
	size_img = "1280x720"
	
	#Create path
	path = '{}/{}.jpg'.format(path, img_name)	
	
	os.system('fswebcam ' + device +' -r ' + size_img + ' -S 3  --no-banner ' + path) # uses Fswebcam to take picture
	
	time.sleep(0.2) # this line creates a 15 second delay before repeating the loop
	
	return path


def Get_Media(times):
	media = list(map(lambda x: x[0], times))
	media = sum(media) / len(media)
	return media		


def ImageAligment(ruta1, ruta2):
	# Read the images to be aligned
	im1 =  cv2.imread(ruta1);
	im2 =  cv2.imread(ruta2)

	# Convert images to grayscale
	im1_gray = cv2.cvtColor(im1,cv2.COLOR_BGR2GRAY)
	im2_gray = cv2.cvtColor(im2,cv2.COLOR_BGR2GRAY)
	
	# Find size of image1   
	sz = im1.shape
	
	# Define the motion model
	warp_mode = cv2.MOTION_TRANSLATION
	
	# Define 2x3 or 3x3 matrices and initialize the matrix to identity
	
	if warp_mode == cv2.MOTION_HOMOGRAPHY :
		warp_matrix = np.eye(3, 3, dtype=np.float32)
	else :
		warp_matrix = np.eye(2, 3, dtype=np.float32)
		
	# Specify the number of iterations.
	number_of_iterations = 5000;
	
	# Specify the threshold of the increment
	# in the correlation coefficient between two iterations
	termination_eps = 1e-10;
	
	# Define termination criteria
	criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, number_of_iterations,  termination_eps)
	
	# Run the ECC algorithm. The results are stored in warp_matrix.
	(cc, warp_matrix) = cv2.findTransformECC (im1_gray,im2_gray,warp_matrix, warp_mode, criteria)
	
	if warp_mode == cv2.MOTION_HOMOGRAPHY :
	
	# Use warpPerspective for Homography
		im2_aligned = cv2.warpPerspective (im2, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
		
	else :
	# Use warpAffine for Translation, Euclidean and Affine
		im2_aligned = cv2.warpAffine(im2, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)

	
	# Show final results
	imagen1 = cv2.imread(ruta1, 1)
	diferenciasImagen = cv2.absdiff(imagen1, im2_aligned)
	
	#Save Img
	cv2.imwrite('img/img_result.jpg',im2_aligned)
	
	
	