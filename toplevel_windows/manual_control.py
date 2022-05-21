from faulthandler import disable
from ossaudiodev import control_labels
from tkinter import *
from tkinter import font
from datetime import datetime
from threading import Thread
import os
import time
from tkinter import messagebox
import RPi.GPIO as GPIO
import pigpio
import sensors_and_data.sensors as sensors
import sensors_and_data.datalogging as datalogging

def destroy_control(ESC):
    speed = 0
    pi.set_servo_pulsewidth(ESC, speed)
    GPIO.cleanup()
    control_toplevel.destroy()

def sensor_data_thread():
    while control_toplevel.winfo_exists() == TRUE:
        sensor_control.sensors_data()

def control(ESC, min_value, max_value, font_size):
    global control_toplevel
    global sensor_control
    control_toplevel = Toplevel()
    control_toplevel.title('Manual Control')
    control_toplevel.attributes('-fullscreen', True)


    control_toplevel.grab_set()

    desired_font = font.Font(size = font_size)

    global pi
    pi = pigpio.pi();

    # Setting a wait button
    var = IntVar()
    i = 0
    button = Button(control_toplevel, text="Yes", command=lambda: var.set(i), font = desired_font)
    button.grid(row=0, column=0, columnspan=6)

    destroy_button = Button(control_toplevel, text="close window", command=lambda: destroy_control(ESC), font = desired_font)
    destroy_button.grid(row=1, column=0, columnspan=6)

    print ("I'm Starting the motor, I hope its calibrated and armed, if not restart by giving 'x'")

    myLabel = Label(control_toplevel, text="Press yes if the esc is calibrated, otherwise close the window")
    myLabel.grid(row=2, column=0, columnspan=6)

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

    ten_decrease_button = Button(control_toplevel, text="<<<", command=lambda: set_esc(speed.get()-100), font = desired_font)
    ten_decrease_button.grid(row=3, column=0)
    one_decrease_button = Button(control_toplevel, text="<<", command=lambda: set_esc(speed.get()-10), font = desired_font)
    one_decrease_button.grid(row=3, column=1)
    slight_decrease_button = Button(control_toplevel, text="<", command=lambda: set_esc(speed.get()-1), font = desired_font)
    slight_decrease_button.grid(row=3, column=2)
    slight_increase_button = Button(control_toplevel, text=">", command=lambda: set_esc(speed.get()+1), font = desired_font)
    slight_increase_button.grid(row=3, column=3)
    one_increase_button = Button(control_toplevel, text=">>", command=lambda: set_esc(speed.get()+10), font = desired_font)
    one_increase_button.grid(row=3, column=4)
    ten_increase_button = Button(control_toplevel, text=">>>", command=lambda: set_esc(speed.get()+100), font = desired_font)
    ten_increase_button.grid(row=3, column=5)

    speedlabel = Label(control_toplevel, text="speed = ")
    speedlabel.grid(row=4, column=0, columnspan=3)
    voltagelabel = Label(control_toplevel, text="voltage = ")
    voltagelabel.grid(row=5, column=0, columnspan=3)
    currentlabel = Label(control_toplevel, text="current = ")
    currentlabel.grid(row=6, column=0, columnspan=3)
    powerlabel = Label(control_toplevel, text="power = ")
    powerlabel.grid(row=7, column=0, columnspan=3)
    thrustlabel = Label(control_toplevel, text="thrust = ")
    thrustlabel.grid(row=8, column=0, columnspan=3)
    esclabel = Label(control_toplevel, text="esc temp = ")
    esclabel.grid(row=9, column=0, columnspan=3)

    speedvalue = Label(control_toplevel, text="NA")
    speedvalue.grid(row=4, column=3, columnspan=3)
    voltagevalue = Label(control_toplevel, text="NA")
    voltagevalue.grid(row=5, column=3, columnspan=3)
    currentvalue = Label(control_toplevel, text="NA")
    currentvalue.grid(row=6, column=3, columnspan=3)
    powervalue = Label(control_toplevel, text="NA")
    powervalue.grid(row=7, column=3, columnspan=3)
    thrustvalue = Label(control_toplevel, text="NA")
    thrustvalue.grid(row=8, column=3, columnspan=3)
    escvalue = Label(control_toplevel, text="NA")
    escvalue.grid(row=9, column=3, columnspan=3)

    sensor_control = sensors.Sensors()
    sensor_control.sensors_start()
    datalog = datalogging.Datalog()
    datalog.make_logfile("Manual")

    sensor_control.sensors_data()
    sensor_thread = Thread(target=sensor_data_thread)
    sensor_thread.start()
    class TempHigh(Exception):
        pass

    class VoltageLow(Exception):
        pass

    while control_toplevel.winfo_exists() == TRUE:
        try:
            data = sensor_control.data
            data["pwm"] = speed.get()
            data["speed"] = (speed.get()-1000)/10

            datalog.log_data(data)

            speedvalue.config(text="%.2f" % data["speed"])
            voltagevalue.config(text="%.2f" % data["voltage"])
            currentvalue.config(text="%.2f" % data["current"])
            powervalue.config(text="%.2f" % data["power"])
            thrustvalue.config(text="%.2f" % data["thrust"])
            escvalue.config(text="%.2f" % data["esc_temp"])

            if data["esc_temp"] > 80:
                raise TempHigh()
            elif data["voltage"] < 21:
                raise VoltageLow()
            for i in range (0,5):
                print("i is")
                print(i)
                control_toplevel.update()
                time.sleep(0.1)

        except TempHigh:
            set_esc(0)
            print ("high temperature alert")
            messagebox.showwarning(mes)
            break

        except VoltageLow:
            set_esc(0)
            print ("battery drain alert")
            break

        except (KeyboardInterrupt, SystemExit):
            set_esc(0)
            print ("battery drain alert")
            break
    set_esc(0)