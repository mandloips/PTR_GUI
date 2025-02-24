from faulthandler import disable
from logging import exception
import os
import time
import sys
from tkinter import font
import pigpio
import RPi.GPIO as GPIO
from datetime import datetime
from smbus2 import SMBus
import toplevel_windows.test_modes as top_test
import toplevel_windows.calibration as top_calib
import toplevel_windows.manual_control as top_control


from tkinter import *

os.system ("sudo pigpiod")
time.sleep(1)
import pigpio


# Setting up parameters for ESC
ESC = 27
max_value = 2000
min_value = 1000
pi = pigpio.pi();

root = Tk()
root.title('PTR')
root.attributes('-fullscreen', True)
# root.iconbitmap('c:/gui/codemy.ico')
# root.geometry("200x150")
font_size = 25
desired_font = font.Font(size = font_size)
 
label = Label(root, text = "Hello UMTian", font = desired_font)
label.pack(padx = 5, pady = 5)

spacing1 = Label(root, text = "    ").pack()
cal_button = Button(root, text="Calibrate", command=lambda: top_calib.calibration(ESC, min_value, max_value, font_size), font = desired_font).pack()

spacing2 = Label(root, text = "    ").pack()
manual_button = Button(root, text="Manual Control", command=lambda: top_control.control(ESC, min_value, max_value, font_size), font = desired_font).pack()

spacing3 = Label(root, text = "    ").pack()
test_button = Button(root, text="Test (Datalogging)", command=lambda: top_test.test(ESC, font_size), font = desired_font).pack()

spacing4 = Label(root, text = "    ").pack()
destroy_root_button = Button(root, text="close window", command=root.destroy, font = desired_font).pack()

root.protocol("WM_DELETE_WINDOW", disable)

mainloop()
