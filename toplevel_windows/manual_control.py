from faulthandler import disable
from tkinter import *
from tkinter import font
from datetime import datetime
import os
import time
import RPi.GPIO as GPIO
import pigpio

def destroy_control(ESC):
        speed = 0
        pi.set_servo_pulsewidth(ESC, speed)
        control_toplevel.destroy()


def control(ESC, min_value, max_value, font_size):
        global control_toplevel
        control_toplevel = Toplevel()
        control_toplevel.title('Manual Control')

        desired_font = font.Font(size = font_size)

        global pi
        pi = pigpio.pi();

        # Setting a wait button
        var = IntVar()
        i = 0
        button = Button(control_toplevel, text="Yes", command=lambda: var.set(i), font = desired_font)
        button.pack()

        destroy_button = Button(control_toplevel, text="close window", command=lambda: destroy_control(ESC), font = desired_font).pack()
        
        print ("I'm Starting the motor, I hope its calibrated and armed, if not restart by giving 'x'")

        myLabel = Label(control_toplevel, text="Press yes if the esc is calibrated, otherwise close the window")
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


        ten_decrease_button = Button(control_toplevel, text="<<", command=lambda: set_esc(speed.get()-100), font = desired_font)
        ten_decrease_button.pack()
        one_decrease_button = Button(control_toplevel, text="<", command=lambda: set_esc(speed.get()-10), font = desired_font)
        one_decrease_button.pack()
        one_increase_button = Button(control_toplevel, text=">", command=lambda: set_esc(speed.get()+10), font = desired_font)
        one_increase_button.pack()
        ten_increase_button = Button(control_toplevel, text=">>", command=lambda: set_esc(speed.get()+100), font = desired_font)
        ten_increase_button.pack()

        str_label = "speed = " + str((speed.get()-1000)/10) + "%"
        myspeedLabel = Label(control_toplevel, text=str_label)
        myspeedLabel.pack()