import os
import time
import cv2 as cv
import numpy as np
from datetime import datetime
# from multiprocessing import Queue
# from multiprocessing import Process
import threading
from queue import Queue

import nanocamera as nano
from libs.mpu6050 import getGyro, getAccel

############### For camera
should_run = True

def write_frame(frQueue, frame_sz, imgDir):
	print('Start writing frame process')
	while should_run:
		if not frQueue.empty():
			ts,frame = frQueue.get()
			# frame=cv.resize(frame,frame_sz)
			imgFileName='%s/%.3f.jpg' % (imgDir,ts)
			# print(imgFileName)
			cv.imwrite(imgFileName, frame)
		time.sleep(0.005)

def read_frame(cmQueue, frQueue):
	cap = nano.Camera(flip=2, width=1080, height=720, fps=30)
	try:
		cap.read()
	except Exception as e:
		print('Exception:', e)

	print('Start reading frame process')
	while should_run:
		if not cmQueue.empty() and cap.isReady():
			#print('read frame')
			ts = cmQueue.get()[0]
			frame = cap.read()
			frQueue.put([ts, frame])
		time.sleep(0.005)
	cap.release()
	del cap

if __name__ == "__main__":
	# cap =getCapture()
	cap = 1
	if cap is None:
		print('Can not init camera')
	else:
		frame_sz = (720, 480)
		dt=datetime.now()
		accelFileName='./data_raw/nhquan4/test/%d%02d%02d_%02d%02d%02d.csv' % (dt.year,dt.month,dt.day,dt.hour, dt.minute,dt.second)
		imgDir='./data_raw/nhquan4/test/%d%02d%02d_%02d%02d%02d' % (dt.year,dt.month,dt.day,dt.hour, dt.minute,dt.second)
		os.makedirs(imgDir, exist_ok=True)
		file = open(accelFileName, "w")
		frQueue = Queue(maxsize=1000)
		cmQueue = Queue(maxsize=1000)

		
		p_readImg = threading.Thread(target=read_frame, args=(cmQueue, frQueue,))
		p_writeImg = threading.Thread(target=write_frame, args=(frQueue, frame_sz, imgDir,))

		
		p_readImg.start()
		p_writeImg.start()

		cv.namedWindow('image', cv.WINDOW_NORMAL)
		k=-1
		status=0 # Waiting
		i=0
		G=1
		while True:
			i=i+1
			ts = time.time()
			if status==1:				
				###### Capture accel		
				ax, ay, az = getAccel()
				gx, gy, gz = getGyro()		
				####### Capture video 
				if cmQueue.empty():									
					cmQueue.put([ts])
				v = '%.3f,%f,%f,%f,%f,%f,%f\n' % (ts, gx, gy, gz, ax, ay, az)
				#print(v)
				file.write(v)
			k = cv.waitKey(2)	
			if k!=-1:
				print(k)	
			if k==27 or k==84 or k==86: # esc or down key
				break
			if (k==82 or k==85) and status==0: # up key
				status=1                                
				file.write('0,0,0,0,0,0,0,0\n')
				k=-1
				print('recording %02d' % (G))
				G=G+1 
			if (k==82 or k==85) and status==1:
				status=1			
				file.write('-1,-1,-1,-1,-1,-1,-1,-1\n')
				k=-1
				print('pause')	
				
		file.close()
		cv.destroyAllWindows()
		time.sleep(3) # wait for flush data
		should_run = False
		#p_readImg.join()
		#p_writeImg.join()		
		print('Finish')
