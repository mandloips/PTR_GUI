from faulthandler import disable
from tkinter import *
from tkinter import font
from datetime import datetime
import os
import time
import RPi.GPIO as GPIO
import pigpio

def calibration(ESC, min_value, max_value, font_size):
        calib_toplevel = Toplevel()
        calib_toplevel.title('Calibrate')
        calib_toplevel.protocol("WM_DELETE_WINDOW", disable)

        calib_toplevel.grab_set()

        desired_font = font.Font(size = font_size)
        pi = pigpio.pi();

        # Setting a wait button
        var = IntVar()
        i = 0
        button = Button(calib_toplevel, text="Done", command=lambda: var.set(i), font = desired_font)
        button.pack()

        pi.set_servo_pulsewidth(ESC, 0)
        print("Disconnect the battery and press done button")
        myLabel = Label(calib_toplevel, text="Disconnect the battery and press done button")
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
        calib_toplevel.update()

        time.sleep(7)
        print ("Wait for it ....")
        time.sleep (5)
        print ("Im working on it, DONT WORRY JUST WAIT.....")
        pi.set_servo_pulsewidth(ESC, 0)
        time.sleep(2)
        print ("Arming ESC now...")

        myLabel.config(text="Arming ESC now...")
        calib_toplevel.update()

        pi.set_servo_pulsewidth(ESC, min_value)
        time.sleep(1)
        print ("See.... uhhhhh")

        myLabel.config(text="I think it is done now...")

        button.destroy()
        button = Button(calib_toplevel, text="close window", command=calib_toplevel.destroy, font = desired_font).pack()