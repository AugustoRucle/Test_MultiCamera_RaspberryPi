#########################  Libraries ######################### 
import cv2
import numpy as np
import os 
import time
import matplotlib.pyplot as plt
from picamera import PiCamera
from time import sleep
from prettytable import PrettyTable

#########################  Functions ######################### 

def GetOptionSelected(option):
	if(option == "P"):
		return "PiCamera_img", None
	elif(option == "U"):
		return None, "USBCamera_img"
	elif(option == "M"):
		return "PiCamera_img", "USBCamera_img"
	return None, None

def Init_PICamera(path):
	times = []
	path_img_1 = TakePicture(camera, path, "img_{}".format(0))	
	
	for i in range(1,1000):
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
	
	return times	
	
def Init_USBCamera(path):
	times = []
	path_img_1 = TakePicture(camera, path, "img_{}".format(0))	
	
	for i in range(1,1000):
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
	
	return times		

def TakePicture(camera, path, img_name, resolution = (640, 480)):
	
	if path == "PiCamera_img":
		return TakePicture_PiCamera(camera, path, img_name, resolution)
		
	elif path == "USBCamera_img":
		return TakePicture_USBCamera(camera, path, img_name)
		

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


def TakePicture_USBCamera(camera, path, img_name):
	size_img = "1280x720"
	
	#Create path
	path = '{}/{}.jpg'.format(path, img_name)	
	
	os.system('fswebcam -r ' + size_img + ' -S 3  --no-banner ' + path) # uses Fswebcam to take picture
	
	time.sleep(0.2) # this line creates a 15 second delay before repeating the loop
	
	return path


def Draw_Bar_Times(times):
	times, iterations = list(zip(*times))
	
	plt.suptitle("Comparación de los tiempos de ejecución", fontsize=12)
	plt.title("para  N=1000 ejecuciones")
	
	plt.ylabel("Tiempo(seg)")
	plt.xlabel("Ejecuciones")
	plt.plot(iterations, times, "bo-", alpha=0.5)
	plt.grid(True)
	plt.show()	


def Draw_Bar_Mean(media):
	n_groups = 2
	fig, ax = plt.subplots()
	index = np.arange(n_groups)
	bar_width, opacity = 0.8, 0.8
	
	plt.suptitle("Comparación de los tiempos de ejecución promedios", fontsize=12)
	plt.title("para  N=1000 ejecuciones")
	plt.bar(index, (media), bar_width, alpha=opacity, color='b')
	plt.ylabel('Tiempo(seg)')
	plt.xlabel('Configuraciones')
	plt.xticks(index, ('Config_1', 'Config_2'))
	plt.grid(True)
	plt.show()


def Print_Times(times):
	table = PrettyTable()
	table.field_names = ["# Ejecución", "Tiempo(Seg)"]
	amount_items = len(times)
	list_times, list_iterations = list(zip(*times))
	
	for i in range(amount_items * 0.2):
		table.add_row((list_iterations[i], list_times[i]))

	for i in range(amount_items * 0.2, 0):
		table.add_row((list_iterations[i-1], list_times[i-1]))
	
	print("\n\n")
	print(table)
	print("\n")
	

def Print_Data(times, start_time, finish_time):
	Print_Times(times)
	print("Media: {}\n".format(Get_Media(times)))
	print("Duration (H:M:S):{!s}\n\n".format(time.strftime("%H:%M:%S", time.gmtime(finish_time - start_time))))


def Get_Media(times):
	media = list(map(lambda x: x[0], times))
	media = sum(media) / len(media)
	return media		

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

	
	# Show final results
	imagen1 = cv2.imread(ruta1, 1)
	diferenciasImagen = cv2.absdiff(imagen1, im2_aligned)
	
	#Save Img
	cv2.imwrite('img/img_result.jpg',im2_aligned)

######################### Main Code ######################### 
camera = PiCamera()

option = input("PICamera(P), USBCamera(U), MultiCamera(M): ")

path_PI, path_USB = GetOptionSelected(option)

times_PI, times_USB = [], []

if(path_PI != None or path_USB != None):

	if(path_PI):
		print("Starting PI")
		start_time = time.time()
		times_PI = Init_PICamera(path_PI)
		finish_time = time.time()

		if(option != "M"):		
			#Draw Chart
		 	Draw_Bar_Times(times_PI)
		 
		 	#Print Data
		 	Print_Data(times_PI, start_time, finish_time)
		 
		 	print("\nFinish PI\n")

	if(path_USB):
		print("Starting USB")
		start_time = time.time()
		times_USB = Init_USBCamera(path_USB)
		finish_time = time.time()	
		
		if(option != "M"):
			#Draw Chart
			Draw_Bar_Times(times_USB)
		
			#Print Data
			Print_Data(times_USB, start_time, finish_time)
			
			print("\nFinish USB\n")
	
	if(path_PI and path_USB):
		################PI
		#Draw Chart
		Draw_Bar_Times(times_PI)
		 
		#Print Data
		Print_Data(times_PI, start_time, finish_time)
		 
		print("\nFinish PI\n")
		 	
		################USB
		#Draw Chart
		Draw_Bar_Times(times_USB)
		
		#Print Data
		Print_Data(times_USB, start_time, finish_time)
			
		print("\nFinish USB\n")
				
		
		media_PI = Get_Media(times_PI)
		media_USB = Get_Media(times_USB)
		
		Draw_Bar_Mean((media_PI, media_USB))
		
	
	
	
	
	
	
	
	