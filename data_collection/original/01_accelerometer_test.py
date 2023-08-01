from time import sleep
import time
from datetime import datetime
import cv2 as cv
import os
from libs.mpu6050 import getGyro, getAccel
import matplotlib.pyplot as plt

if __name__ == "__main__":	
	cv.namedWindow('image', cv.WINDOW_NORMAL)
	k=-1
	acce_data={}
	acce_data['gx']=[]
	acce_data['gy']=[]
	acce_data['gz']=[]
	acce_data['ax']=[]
	acce_data['ay']=[]
	acce_data['az']=[]
	fig = plt.figure(figsize=(15,5))
	plt.ion()
	ax1 = fig.add_subplot(211) # for acce	
	ax2 = fig.add_subplot(212) # for acce	
	plt.show()		
	while True: 	
		ts = time.time()					
		###### Capture accel		
		ax, ay, az = getAccel()
		gx, gy, gz = getGyro()	
		acce_data['gx'].append(gx)
		acce_data['gy'].append(gy)
		acce_data['gz'].append(gz)  
		acce_data['ax'].append(ax)
		acce_data['ay'].append(ay)
		acce_data['az'].append(az) 
		# v='%.3f,%f,%f,%f,%f,%f,%f\n' % (ts, gx, gy, gz, ax, ay, az )
		# print(v)
		ax1.clear()
		ax1.set_xlim(left=0, right=len(acce_data['gx'])+10)
		ax1.plot(acce_data['gx'][-200:], color='r', label='gx')
		ax1.plot(acce_data['gy'][-200:], color='g',label='gy')
		ax1.plot(acce_data['gz'][-200:], color='b',label='gz')
		ax1.legend(loc='upper right')

		ax2.clear()
		ax2.set_xlim(left=0, right=len(acce_data['gx'])+10)
		ax2.plot(acce_data['ax'][-200:], color='y', label='ax')
		ax2.plot(acce_data['ay'][-200:], color='m',label='ay')
		ax2.plot(acce_data['az'][-200:], color='c',label='az')
		ax2.legend(loc='upper right')
		plt.pause(0.001)