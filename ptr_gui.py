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
desired_font = font.Font(size = 25)
 
label = Label(root, text = "Hello UMTian", font = desired_font)
label.pack(padx = 5, pady = 5)
        
def calibration():
        top = Toplevel()
        top.title('Calibrate')
        top.protocol("WM_DELETE_WINDOW", disable)

        # Setting a wait button
        var = IntVar()
        i = 0
        button = Button(top, text="Done", command=lambda: var.set(i), font = desired_font)
        button.pack()

        pi.set_servo_pulsewidth(ESC, 0)
        print("Disconnect the battery and press done button")
        myLabel = Label(top, text="Disconnect the battery and press done button")
        myLabel.pack()

        # Waiting for button to be pressed
        i+=1
        button.wait_variable(var)

        pi.set_servo_pulsewidth(ESC, max_value)
        print("Connect the battery NOW.. you will here two beeps, then wait for a gradual falling tone then press Enter")
        myLabel.config(text="Connect the battery NOW.. enjoy the music and then press the Done button")

        # Waiting for button to be pressed
        i+=1
        button.wait_variable(var)

        pi.set_servo_pulsewidth(ESC, min_value)
        print ("Wierd eh! Special tone")

        myLabel.config(text="Im working on it now...")
        top.update()

        time.sleep(7)
        print ("Wait for it ....")
        time.sleep (5)
        print ("Im working on it, DONT WORRY JUST WAIT.....")
        pi.set_servo_pulsewidth(ESC, 0)
        time.sleep(2)
        print ("Arming ESC now...")

        myLabel.config(text="Arming ESC now...")
        top.update()

        pi.set_servo_pulsewidth(ESC, min_value)
        time.sleep(1)
        print ("See.... uhhhhh")

        myLabel.config(text="I think it is done now...")

        button.destroy()
        button = Button(top, text="close window", command=top.destroy, font = desired_font).pack()
        


        # time.sleep(15)
        # top.destroy()

def destroy_control():
        speed = 0
        pi.set_servo_pulsewidth(ESC, speed)
        top.destroy()



def control():
        global top
        top = Toplevel()
        top.title('Manual Control')

        # Setting a wait button
        var = IntVar()
        i = 0
        button = Button(top, text="Yes", command=lambda: var.set(i), font = desired_font)
        button.pack()

        destroy_button = Button(top, text="close window", command=destroy_control, font = desired_font).pack()
        
        print ("I'm Starting the motor, I hope its calibrated and armed, if not restart by giving 'x'")

        myLabel = Label(top, text="Press yes if the esc is calibrated, otherwise close the window")
        myLabel.pack()

        # Waiting for button to be pressed
        i+=1
        button.wait_variable(var)
        myLabel.destroy()

        time.sleep(1)
        speed = IntVar()
        speed.set(min_value)
        pi.set_servo_pulsewidth(ESC, speed.get())

        

        def set_esc(value):
                if value >= min_value and value <= max_value:
                        speed.set(value)
                elif value <= min_value:
                        speed.set(min_value)
                elif value >= max_value:
                        speed.set(max_value)
                
                pi.set_servo_pulsewidth(ESC, speed.get())
                print(speed.get())

                str_label = "speed = " + str((speed.get()-1000)/10) + "%"
                myspeedLabel.config(text = str_label)


        ten_decrease_button = Button(top, text="<<", command=lambda: set_esc(speed.get()-100), font = desired_font)
        ten_decrease_button.pack()
        one_decrease_button = Button(top, text="<", command=lambda: set_esc(speed.get()-10), font = desired_font)
        one_decrease_button.pack()
        one_increase_button = Button(top, text=">", command=lambda: set_esc(speed.get()+10), font = desired_font)
        one_increase_button.pack()
        ten_increase_button = Button(top, text=">>", command=lambda: set_esc(speed.get()+100), font = desired_font)
        ten_increase_button.pack()

        str_label = "speed = " + str((speed.get()-1000)/10) + "%"
        myspeedLabel = Label(top, text=str_label)
        myspeedLabel.pack()

        # time.sleep(10)

        # while True:
        #         pi.set_servo_pulsewidth(ESC, speed.get())
        #         print(speed.get())



cal_button = Button(root, text="Calibrate", command=lambda: top_calib.calibration(ESC, min_value, max_value), font = desired_font).pack()
manual_button = Button(root, text="Manual Control", command=control, font = desired_font).pack()
test_button = Button(root, text="Test (Datalogging)", command=lambda: top_test.test(ESC), font = desired_font).pack()
destroy_root_button = Button(root, text="close window", command=root.destroy, font = desired_font).pack()

root.protocol("WM_DELETE_WINDOW", disable)

mainloop()