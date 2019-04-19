#########################  Libraries ######################### 
import time
import matplotlib.pyplot as plt
from prettytable import PrettyTable
from myThread import Camera
from picamera import PiCamera
import numpy as np


#########################  Functions ######################### 

def GetPath(option):
	if(option == "P"):
		return "PiCamera_img", None
	elif(option == "U"):
		return None, "USBCamera_img"
	elif(option == "M" or option == "A"):
		return "PiCamera_img", "USBCamera_img"
	return None, None

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
	n_groups = 4
	fig, ax = plt.subplots()
	index = np.arange(n_groups)
	bar_width, opacity = 0.5, 0.8
	
	plt.suptitle("Comparación de los tiempos de ejecución promedios", fontsize=12)
	plt.title("para  N=1000 ejecuciones")
	plt.bar(index, (media), bar_width, alpha=opacity, color='b')
	plt.ylabel('Tiempo(seg)')
	plt.xlabel('Configuraciones')
	plt.xticks(index, ('Config_1', 'Config_2', 'Config_4 PI', 'Config_4 USB'))
	plt.grid(True)
	plt.show()


def Print_Times(times):
	table = PrettyTable()
	table.field_names = ["# Ejecución", "Tiempo(Seg)"]
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

######################### Main Code ######################### 
camera = PiCamera()

option = input("PICamera(P), USBCamera(U), MultiCamera(M), All(A): ")

path_PI, path_USB = GetPath(option)

times_PI, times_USB, times_PI_Multi, times_USB_Multi = [], [], [], []


if(path_PI != None or path_USB != None):

	if(option == "P" or option == "A"):
		print("Starting PI")
		start_time = time.time()
		pi_camera = Camera("PI_Camera thread", times_PI, path_PI, camera)
		pi_camera.start()
		pi_camera.join()
		finish_time = time.time()

		if(option != "A"):	
			print("Impriendo datos de PI_Camera")	
			#Draw Chart
			Draw_Bar_Times(times_PI)
			
			#Print Data
			Print_Data(times_PI, start_time, finish_time)
		 
		print("\nFinish PI\n")

	if(option == "U" or option == "A"):
		print("Starting USB")
		start_time = time.time()
		usb_camera = Camera("USB_Camera thread", times_USB, path_USB, camera)
		usb_camera.start()
		usb_camera.join()
		finish_time = time.time()	
		
		if(option != "A"):
			
			print("Impriendo datos de USB_Camera")			
			
			#Draw Chart
			Draw_Bar_Times(times_USB)
		
			#Print Data
			Print_Data(times_USB, start_time, finish_time)
			
		print("\nFinish USB\n")
	
	if(option == "M" or option == "A"):	
		
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
			print("\nPrint Data PI\n")
		
			#Draw Chart
			Draw_Bar_Times(times_PI)
		 
			#Print Data
			Print_Data(times_PI)
		
			################ USB
			print("\nPrint Data USB\n")
		
			#Draw Chart
			Draw_Bar_Times(times_USB)
		
			#Print Data
			Print_Data(times_USB)
	
	if(option == "A"):
		media_PI = Get_Media(times_PI)
		media_USB = Get_Media(times_USB)
		media_PI_Multi = Get_Media(times_PI_Multi)
		media_USB_Multi = Get_Media(times_USB_Multi)
		
		############### PI
		print("\nPrint Data PI\n")
		
		#Draw Chart
		Draw_Bar_Times(times_PI)
		 
		#Print Data
		Print_Data(times_PI)
	
		################ USB
		print("\nPrint Data USB\n")
		
		#Draw Chart
		Draw_Bar_Times(times_USB)
		
		#Print Data
		Print_Data(times_USB)
		
		############### PI Multi
		print("\nPrint Data PI Multi\n")
		
		#Draw Chart
		Draw_Bar_Times(times_PI_Multi)
		 
		#Print Data
		Print_Data(times_PI_Multi)
	
		################ USB Multi
		print("\nPrint Data USB Multi\n")
		
		#Draw Chart
		Draw_Bar_Times(times_USB_Multi)
		
		#Print Data
		Print_Data(times_USB_Multi)
		
		Draw_Bar_Mean((media_PI, media_USB, media_PI_Multi, media_USB_Multi))
		
	