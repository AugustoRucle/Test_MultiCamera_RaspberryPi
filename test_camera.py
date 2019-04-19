#########################  Libraries ######################### 
import time
import matplotlib.pyplot as plt
from prettytable import PrettyTable
from myThread import Camera

#########################  Functions ######################### 

def GetOptionSelected(option):
	if(option == "P"):
		return "PiCamera_img", None
	elif(option == "U"):
		return None, "USBCamera_img"
	elif(option == "M"):
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

######################### Main Code ######################### 

option = input("PICamera(P), USBCamera(U), MultiCamera(M): ")

path_PI, path_USB = GetOptionSelected(option)

times_PI, times_USB = [], []


if(path_PI != None or path_USB != None):

	if(path_PI):
		print("Starting PI")
		start_time = time.time()
		pi_camera = Camera("PI_Camera thread", times_PI, path_PI)
        pi_camera.start()
        pi_camera.join()
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
        usb_camera = Camera("USB_Camera thread", times_USB, path_USB)
        usb_camera.start()
        usb_camera.join()
		finish_time = time.time()	
		
		if(option != "M"):
			#Draw Chart
			Draw_Bar_Times(times_USB)
		
			#Print Data
			Print_Data(times_USB, start_time, finish_time)
			
		print("\nFinish USB\n")
	
	if(path_PI and path_USB):

        

		################ PI
		#Draw Chart
		Draw_Bar_Times(times_PI)
		 
		#Print Data
		Print_Data(times_PI, start_time, finish_time)
		 
		print("\nFinish PI\n")
		 	
		################ USB
		#Draw Chart
		Draw_Bar_Times(times_USB)
		
		#Print Data
		Print_Data(times_USB, start_time, finish_time)
			
		print("\nFinish USB\n")
				
		
		media_PI = Get_Media(times_PI)
		media_USB = Get_Media(times_USB)
		
		Draw_Bar_Mean((media_PI, media_USB))
		
	