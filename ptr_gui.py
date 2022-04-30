from faulthandler import disable
from logging import exception
import os
import time
import sys
from tkinter import font
import pigpio
import threading
import RPi.GPIO as GPIO
import Motor_Control.data_collection
from time import sleep
from datetime import datetime
from smbus2 import SMBus
from mlx90614 import MLX90614
import Top_Windows.test_modes as top_test
import Top_Windows.calibration as top_calib
import Top_Windows.manual_control as top_control


from tkinter import *

os.system ("sudo pigpiod")
time.sleep(1)
import pigpio


# Setting up parameters for ESC
ESC=27
max_value = 2000
min_value = 1000
pi = pigpio.pi();

root = Tk()
root.title('PTR')
# root.iconbitmap('c:/gui/codemy.ico')
# root.geometry("200x150")
font_size = 25
desired_font = font.Font(size = font_size)
 
label = Label(root, text = "Hello UMTian", font = desired_font)
label.pack(padx = 5, pady = 5)

cal_button = Button(root, text="Calibrate", command=lambda: top_calib.calibration(ESC, min_value, max_value, font_size), font = desired_font).pack()
manual_button = Button(root, text="Manual Control", command=lambda: top_control.control(ESC, min_value, max_value, font_size), font = desired_font).pack()
test_button = Button(root, text="Test (Datalogging)", command=lambda: top_test.test(ESC, font_size), font = desired_font).pack()
destroy_root_button = Button(root, text="close window", command=root.destroy, font = desired_font).pack()

root.protocol("WM_DELETE_WINDOW", disable)

mainloop()