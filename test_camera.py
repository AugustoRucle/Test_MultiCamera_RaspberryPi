#########################  Libraries ######################### 
import time
import matplotlib.pyplot as plt
from prettytable import PrettyTable
from myThread2 import Camera
from picamera import PiCamera
import numpy as np


#########################  Functions ######################### 

def GetPath(option):
	if(option == "P"):
		return "PiCamera_img", None
	elif(option == "U" or option == "TU"):
		return None, "USBCamera_img"
	elif(option == "M" or option == "A" or option == "TC"):
		return "PiCamera_img", "USBCamera_img"
	return None, None


def Draw_Plot_Times(times, title="Comparación de los tiempos de ejecución", subtitle = "para  N=1000 ejecuciones"):
	times, iterations = list(zip(*times))
	
	plt.suptitle(title, fontsize=12)
	plt.title(subtitle)
	
	plt.ylabel("Tiempo(ms)")
	plt.xlabel("Ejecuciones")
	plt.plot(iterations, times, "bo-", alpha=0.5)
	plt.grid(True)
	plt.show()	
	



def Draw_Bar_Mean(media, title="Comparación de los tiempos de ejecución promedios", subtitle = "para  N=1000 ejecuciones"):
	n_groups = 9
	fig, ax = plt.subplots()
	index = np.arange(n_groups)
	bar_width, opacity = 0.5, 0.8
	
	plt.suptitle(title, fontsize=12)
	plt.title(subtitle)
	plt.bar(index, (media), bar_width, alpha=opacity, color='b')
	plt.ylabel('Tiempo(ms)')
	plt.xlabel('Configuraciones')
	plt.xticks(index, ('Config_1 PI', 'Config_2 USB', 'Config_3 USB0', 'Config_3 USB1', 'Config_4 PI', 'Config_4 USB', 'Config_5 PI', 'Config_5 USB0', 'Config_5 USB1'))
	plt.grid(True)
	plt.show()


def Print_Times(times):
	table = PrettyTable()
	table.field_names = ["# Ejecución", "Tiempo(ms)"]
	amount_items, N = len(times), int(len(times) * 0.4)
	list_times, list_iterations = list(zip(*times))
	
	for i in range(N):
		table.add_row((list_iterations[i], list_times[i]))

	for i in range(1, N):
		table.add_row((list_iterations[amount_items-i], list_times[amount_items-i]))
	
	print("\n\n")
	print(table)
	print("\n")
	

def Print_Data(times):
	Print_Times(times)
	print("Media: {}\n".format(Get_Media(times)))
	

def Get_Media(times):
	media = list(map(lambda x: x[0], times))
	media = sum(media) / len(media)
	return media	

def Info_Camera(times, message="Impriendo Informacion de la camara", msg_title = "", msg_sub =""):
	print(message)	
	
	#Draw Chart
	Draw_Plot_Times(times, subtitle = msg_sub)
			
	#Print Data
	Print_Data(times)	

######################### Main Code ######################### 
camera = PiCamera()

option = input("PICamera(P), USBCamera(U), MultiCameras(M), Two_USBCamera(TU), Two_Camera(TC), All(A): ")

path_PI, path_USB = GetPath(option)

times_PI, times_USB = [], []
times_PI_Multi, times_USB_Multi =  [], []
times_USB_Camera_0, times_USB_Camera_1  = [], []
times_PI_All, times_USB_Camera0_All, times_USB_Camera1_All = [], [], []

if(path_PI != None or path_USB != None):

	if(option == "P" or option == "A"):
		print("################################################# Starting PI #################################################")
		
		start_time = time.time()
		pi_camera = Camera("PI_Camera thread", times_PI, path_PI, camera)
		pi_camera.start()
		pi_camera.join()
		finish_time = time.time()

		if(option != "A"):	
			Info_Camera(times_PI, "\nImpriendo datos de PI_Camera\n")
		 
		print("\n################################################# Finish PI #################################################\n")

	if(option == "U" or option == "A"):
		print("################################################# Starting USB #################################################")
		
		start_time = time.time()
		usb_camera = Camera("USB_Camera thread", times_USB, path_USB, camera)
		usb_camera.start()
		usb_camera.join()
		finish_time = time.time()	
		
		if(option != "A"):
			Info_Camera(times_USB, "\nImpriendo datos de USB_Camera\n")
			
		print("\n################################################# Finish USB #################################################\n")
	
	if(option == "TU" or option == "A"):
		print("################################################# Two USB #################################################")
		
		#Init PI
		usb_camera0 = Camera("USB_Camera0 thread", times_USB_Camera_0, path_USB + "/camera0", camera)

		#Init USB		
		usb_camera1 = Camera("USB_Camera1 thread", times_USB_Camera_1 , path_USB + "/camera1", camera)

		#Start thread
		usb_camera0.start()
		usb_camera1.start()

		#Wait for other threads
		usb_camera0.join()
		usb_camera1.join()			

		if(option != "A"):
			############### USB Camera 0
			Info_Camera(times_USB_Camera_0, "\nImpriendo datos de USB_Camera0\n")
		
			################ USB Camera 1
			Info_Camera(times_USB_Camera_1, "\nImpriendo datos de USB_Camera1\n")

			
		print("\n################################################# Finish Two USB #################################################\n")	
	
	if(option == "TC" or option == "A"):	
		print("################################################# Two Cameras #################################################")
		#Init PI
		pi_camera = Camera("PI_Camera thread", times_PI_Multi, path_PI, camera)

		#Init USB		
		usb_camera = Camera("USB_Camera thread", times_USB_Multi, path_USB, camera)
		
		#Start thread
		pi_camera.start()
		usb_camera.start()

		#Wait for other threads
		pi_camera.join()
		usb_camera.join()
		
		if(option != "A"):
			
			############### PI

			Info_Camera(times_PI_Multi, "\nImpriendo datos de PI Camera\n")
		
			################ USB
			Info_Camera(times_USB_Multi, "\nImpriendo datos de USB Camera\n")
			
		print("\n################################################# Finish Two cameras #################################################\n")

	if(option == "M" or option == "A"):	
		print("################################################# Multi #################################################")
		#Init PI
		pi_camera = Camera("PI_Camera thread", times_PI_All, path_PI, camera)

		#Init USB0		
		usb_camera0 = Camera("USB_Camera0 thread", times_USB_Camera0_All, path_USB + "/camera0", camera)
		
		#Init USB1		
		usb_camera1 = Camera("USB_Camera1 thread", times_USB_Camera1_All, path_USB + "/camera1", camera)
		
		#Start thread
		pi_camera.start()
		usb_camera0.start()
		usb_camera1.start()

		#Wait for other threads
		pi_camera.join()
		usb_camera0.join()
		usb_camera1.join()
		
		if(option != "A"):
			
			############### PI

			Info_Camera(times_PI_All, "\nImpriendo datos de PI Camera\n")
		
			################ USB
			Info_Camera(times_USB_Camera0_All, "\nImpriendo datos de USB Camera0\n")
			
			################ USB
			Info_Camera(times_USB_Camera1_All, "\nImpriendo datos de USB Camera1\n")
			
		print("\n################################################# Finish Multi #################################################\n")
	
	if(option == "A"):

		media_PI = Get_Media(times_PI)
		media_USB = Get_Media(times_USB)
		media_USB0 = Get_Media(times_USB_Camera_0)
		media_USB1 = Get_Media(times_USB_Camera_1 )
		media_PI_Multi = Get_Media(times_PI_Multi)
		media_USB_Multi = Get_Media(times_USB_Multi)
		media_PI_All = Get_Media(times_PI_All)
		media_USB0_All = Get_Media(times_USB_Camera0_All)
		media_USB1_All = Get_Media(times_USB_Camera1_All)
		
		############### PI
		
		Info_Camera(times_PI, "\nImpriendo datos de (P)PI Camera\n", msg_sub="Configuración 1")
	
		################ USB
		
		Info_Camera(times_USB, "\nImpriendo datos de (U)USB Camera\n", msg_sub="Configuración 2")
		
		############### USB0
		
		Info_Camera(times_USB_Camera_0, "\nImpriendo datos de (TU)USB Camera 0\n", msg_sub="Configuración 3 USB0")
	
		################ USB1
		Info_Camera(times_USB_Camera_1, "\nImpriendo datos de (TU)USB Camera 1\n", msg_sub="Configuración 3 USB1")
		
		############### PI Two
		
		Info_Camera(times_PI_Multi, "\nImpriendo datos de (TC)Multi Pi Camera\n", msg_sub="Configuración 4 PI ")
	
		################ USB Two

		Info_Camera(times_USB_Multi, "\nImpriendo datos de (TC)Multi USB Camera\n", msg_sub="Configuración 4 USB")
		
		############### PI Multi
		
		Info_Camera(times_PI_All, "\nImpriendo datos de (M)Multi Pi Camera\n", msg_sub="Configuración 5 PI Multi")
	
		################ USB0 Multi

		Info_Camera(times_USB_Camera0_All, "\nImpriendo datos de (M)Multi USB0 Camera\n", msg_sub="Configuración 5 USB0 Multi")
		
		################ USB1 Multi

		Info_Camera(times_USB_Camera1_All, "\nImpriendo datos de (M)Multi USB1 Camera\n", msg_sub="Configuración 5 USB1 Multi")
		
		Draw_Bar_Mean((media_PI, media_USB, media_USB0, media_USB1, media_PI_Multi, media_USB_Multi, media_PI_All, media_USB0_All, media_USB1_All))
		
	