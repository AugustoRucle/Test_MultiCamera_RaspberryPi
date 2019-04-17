# Libraries
import cv2
import numpy as np
import time
from picamera import PiCamera
from time import sleep

# Functions

def GetOptionSelected(option):
	if(option == "P"):
		return "PiCamera_img"
	elif(option == "U"):
		return "USBCamera_img"
	elif(option == "M"):
		return "MultiCamera_img"
	return None

def TakePicture_PiCamera(camera, ruta, img_name):

	#Create path
	path = '{}/{}.jpg'.format(ruta, img_name)	
	
	#Setting camera
	camera.rotation = 180
	camera.resolution = (2592, 1944)
	
	# Camera warm-up time
	sleep(3)
	
	#Capture picture
	camera.capture(path)
	
	return path

def ShowImage(name_window, img):
	cv2.namedWindow(name_window, cv2.WINDOW_NORMAL)
	cv2.imshow(name_window, img)

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
		
	#Show results
	#ShowImage("Image 1", im1)
	#ShowImage("Image 2", im2)
	#ShowImage("Image 3", im2_aligned)
	#cv2.waitKey(0)
	
	# Show final results
	imagen1 = cv2.imread(ruta1, 1)
	diferenciasImagen = cv2.absdiff(imagen1, im2_aligned)
	
	#Save Img
	cv2.imwrite('img/img_result.jpg',im2_aligned)

# Main Code
camera = PiCamera()

option = input("PICamera(P), USBCamera(U), MultiCamera(M): ")

path = GetOptionSelected(option)

if(path != None):

	cronometro = time.time()	
	
	print("Start")
	
	for i in range(1000):
		path_img = TakePicture_PiCamera(camera, path, "img_{}".format(i))
	
	
	print("Finished")
	print("Duracion (H:M:S):{!s}".format(time.strftime("%H:%M:%S", time.gmtime(time.time() - cronometro))))
