from faulthandler import disable
from tkinter import *
from tkinter import font
from datetime import datetime
import os
import time
import RPi.GPIO as GPIO
import pigpio
import sensors_and_data.sensors as sensors

def destroy_control(ESC):
        speed = 0
        pi.set_servo_pulsewidth(ESC, speed)
        control_toplevel.destroy()


def control(ESC, min_value, max_value, font_size):
        global control_toplevel
        control_toplevel = Toplevel()
        control_toplevel.title('Manual Control')

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

        ten_decrease_button = Button(control_toplevel, text="<<", command=lambda: set_esc(speed.get()-100), font = desired_font)
        ten_decrease_button.grid(row=3, column=0)
        one_decrease_button = Button(control_toplevel, text="<", command=lambda: set_esc(speed.get()-10), font = desired_font)
        one_decrease_button.grid(row=3, column=1)
        slight_decrease_button = Button(control_toplevel, text="<", command=lambda: set_esc(speed.get()-1), font = desired_font)
        slight_decrease_button.grid(row=3, column=2)
        slight_increase_button = Button(control_toplevel, text=">", command=lambda: set_esc(speed.get()+1), font = desired_font)
        slight_increase_button.grid(row=3, column=3)
        one_increase_button = Button(control_toplevel, text=">", command=lambda: set_esc(speed.get()+10), font = desired_font)
        one_increase_button.grid(row=3, column=4)
        ten_increase_button = Button(control_toplevel, text=">>", command=lambda: set_esc(speed.get()+100), font = desired_font)
        ten_increase_button.grid(row=3, column=5)

        speedlabel = Label(control_toplevel, text="speed = ")
        speedlabel.grid(row=4, column=0, columnspan=3)
        voltagelabel = Label(control_toplevel, text="voltage = ")
        voltagelabel.grid(row=5, column=0, columnspan=3)
        currentlabel = Label(control_toplevel, text="current = ")
        currentlabel.grid(row=6, column=0, columnspan=3)
        powerlabel = Label(control_toplevel, text="power = ")
        powerlabel.grid(row=7, column=0, columnspan=3)

        speedvalue = Label(control_toplevel, text="NA")
        speedvalue.grid(row=4, column=3, columnspan=3)
        voltagevalue = Label(control_toplevel, text="NA")
        voltagevalue.grid(row=5, column=3, columnspan=3)
        currentvalue = Label(control_toplevel, text="NA")
        currentvalue.grid(row=6, column=3, columnspan=3)
        powervalue = Label(control_toplevel, text="NA")
        powervalue.grid(row=7, column=3, columnspan=3)

        sensor_control = sensors.Sensors()
        sensor_control.sensors_start()

        while control_toplevel.winfo_exists() == TRUE:
                now = datetime.now()
                sensor_control.sensors_data()
                data = {}
                data["timestamp"] = str(now)
                data["amb_temp"] = 'sensor.get_ambient()'
                data["motor_temp"] = "sensor.get_object_1()"
                data["thrust"] = 'hx.get_weight(5)'
                data["voltage"] = sensor_control.voltage
                data["current"] = sensor_control.current
                data["power"] = sensor_control.power
                data["rpm"] = 'rpm'
                data["pwm"] = speed.get()
                data["speed"] = (speed.get()-1000)/10
                
                speedvalue.config(text="%.2f" % data["speed"])
                voltagevalue.config(text="%.2f" % data["voltage"])
                currentvalue.config(text="%.2f" % data["current"])
                powervalue.config(text="%.2f" % data["power"])

                control_toplevel.update()
                time.sleep(0.1)