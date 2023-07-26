import smbus
import math
from time import sleep
import time
import socket   
import datetime
import os
import csv      

# DEV_ADDR = 0x53
DEV_ADDR = 0x68

ACCEL_XOUT = 0x3b
ACCEL_YOUT = 0x3d
ACCEL_ZOUT = 0x3f
TEMP_OUT = 0x41
GYRO_XOUT = 0x43
GYRO_YOUT = 0x45
GYRO_ZOUT = 0x47

PWR_MGMT_1 = 0x6b
PWR_MGMT_2 = 0x6c   

bus = smbus.SMBus(1)
time.sleep(0.2)
bus.write_byte_data(DEV_ADDR, 0x6B, 0x80) # RESET
time.sleep(0.25)
bus.write_byte_data(DEV_ADDR, 0x6B, 0x00) # RESET
time.sleep(0.25)
bus.write_byte_data(DEV_ADDR, 0x6A, 0x07) # RESET
time.sleep(0.25)
bus.write_byte_data(DEV_ADDR, 0x6A, 0x00) # RESET
time.sleep(0.25)
bus.write_byte_data(DEV_ADDR, 0x1A, 0x00) # CONFIG
bus.write_byte_data(DEV_ADDR, 0x1B, 0x18) # +-2000°/s
# bus.write_byte_data(DEV_ADDR, 0x1B, 0x10) # +-1000°/s
bus.write_byte_data(DEV_ADDR, 0x1C, 0x08) # +-4g
time.sleep(0.1)

def read_word(adr):
    high = bus.read_byte_data(DEV_ADDR, adr)
    low = bus.read_byte_data(DEV_ADDR, adr+1)
    val = (high << 8) + low
    return val

def read_word_sensor(adr):
    val = read_word(adr)
    if (val >= 0x8000):  return -((65535 - val) + 1)
    else:  return val

def get_temp():
    temp = read_word_sensor(TEMP_OUT)
    x = temp / 340 + 36.53      # data sheet(register map)
    return x

def getGyro():
    # +-1000°/s
    # x = read_word_sensor(GYRO_XOUT)/ 32.8
    # y = read_word_sensor(GYRO_YOUT)/ 32.8
    # z = read_word_sensor(GYRO_ZOUT)/ 32.8

    # +-2000°/s
    x = read_word_sensor(GYRO_XOUT) / 16.4
    y = read_word_sensor(GYRO_YOUT) / 16.4
    z = read_word_sensor(GYRO_ZOUT) / 16.4
    return [x, y, z]

def getAccel():
    x = read_word_sensor(ACCEL_XOUT)/ 8192
    y= read_word_sensor(ACCEL_YOUT)/ 8192
    z= read_word_sensor(ACCEL_ZOUT)/ 8192
    return [x, y, z]
 
# file = open("accel_data.csv", "w")
# while(True):
#     for i in range(100):
#         ts = int(time.time())
#         ax, ay, az = getAccel()
#         gx, gy, gz = getGyro()
#         #client()
#         print ('{0:4.3f},   {0:4.3f},    {0:4.3f},     {0:4.3f},      {0:4.3f},      {0:4.3f},' .format(gx, gy, gz, ax, ay, az))
#         file.write(str(ts)+ "," +str(gx) + "," + str(gy) + "," + str(gz) + "," + str(ax) + "," + str(ay) + "," + str(az) + "\n")  
#         time.sleep(0.02)
#     break
# file.close()

