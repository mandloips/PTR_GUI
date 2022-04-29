from faulthandler import disable
from logging import exception
import os
import time
import sys
from tkinter import font
from tkinter.font import Font
import pigpio
import threading
import RPi.GPIO as GPIO
import data_collection
from time import sleep
from datetime import datetime
from smbus2 import SMBus
from mlx90614 import MLX90614

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
# root.option_add('*Font', 50)
# root.geometry("200x150")
desired_font = font.Font(size = 25)
 
label = Label(root, text = "Hello UMTian", font = desired_font)
label.pack(padx = 5, pady = 5)


class Pulse(threading.Thread):
        MAX_VALUE = 1300        # if you are changing here then change for calibration too
        MIN_VALUE = 1000        # if you are changing here then change for calibration too
        speed = 0       
        def __init__(self):
                threading.Thread.__init__(self)
                self.speed = 0
                self.pi = pigpio.pi();
                self.pi.set_servo_pulsewidth(ESC, self.speed)
                self.not_exited = True
        def run(self):
                print ("I'm Starting the motor (in 3 seconds), I hope its calibrated and armed, if not stop the testing")
                time.sleep(3)
                print ("test started")

                # initiating the motor
                self.speed = self.MIN_VALUE
                self.pi.set_servo_pulsewidth(ESC, self.speed)
                print ("speed = %d for 3 seconds" % self.speed)
                time.sleep(3)

                # loop for increasing the speed
                while self.speed < self.MAX_VALUE and self.not_exited:
                        self.speed += 1
                        self.pi.set_servo_pulsewidth(ESC, self.speed)

                        if self.speed % 100 == 0:
                                print ("speed = %d for 3 seconds" % self.speed)
                                time.sleep(3)
                        else:
                                time.sleep(0.03)
                
                
                
                while self.speed > self.MIN_VALUE and self.not_exited:
                        self.speed -= 1
                        self.pi.set_servo_pulsewidth(ESC, self.speed)
                        
                        if self.speed % 100 == 0:
                                print ("speed = %d for 3 seconds" % self.speed)
                                time.sleep(3)
                        else:
                                time.sleep(0.03)
        
                self.speed = 0
                self.pi.set_servo_pulsewidth(ESC, self.speed)
                self.pi.stop()
                print("i am running")
        def stop(self):
                print("Stopping\n")
                self.not_exited = False

class Fifty(threading.Thread):
        MAX_VALUE = 1200        # if you are changing here then change for calibration too
        MIN_VALUE = 1000        # if you are changing here then change for calibration too
        speed = 0       
        def __init__(self):
                threading.Thread.__init__(self)
                self.speed = 0
                self.pi = pigpio.pi();
                self.pi.set_servo_pulsewidth(ESC, self.speed)
                self.not_exited = True
        def run(self):
                print ("I'm Starting the motor (in 3 seconds), I hope its calibrated and armed, if not stop the testing")
                time.sleep(3)
                print ("test started")

                # initiating the motor
                self.speed = self.MIN_VALUE
                self.pi.set_servo_pulsewidth(ESC, self.speed)
                print ("speed = %d for 3 seconds" % self.speed)
                time.sleep(3)

                # loop for increasing the speed
                while self.speed < self.MAX_VALUE and self.not_exited:
                        self.speed += 1
                        self.pi.set_servo_pulsewidth(ESC, self.speed)

                        if self.speed % 100 == 0:
                                print ("speed = %d for 3 seconds" % self.speed)
                                time.sleep(3)
                        else:
                                time.sleep(0.03)
                
                
                
                while self.speed > self.MIN_VALUE and self.not_exited:
                        self.speed -= 1
                        self.pi.set_servo_pulsewidth(ESC, self.speed)
                        
                        if self.speed % 100 == 0:
                                print ("speed = %d for 3 seconds" % self.speed)
                                time.sleep(3)
                        else:
                                time.sleep(0.03)
        
                self.speed = 0
                self.pi.set_servo_pulsewidth(ESC, self.speed)
                self.pi.stop()
                print("i am running")
        def stop(self):
                print("Stopping\n")
                self.not_exited = False

class Hundred(threading.Thread):
        MAX_VALUE = 1200        # if you are changing here then change for calibration too
        MIN_VALUE = 1000        # if you are changing here then change for calibration too
        speed = 0       
        def __init__(self):
                threading.Thread.__init__(self)
                self.speed = 0
                self.pi = pigpio.pi();
                self.pi.set_servo_pulsewidth(ESC, self.speed)
                self.not_exited = True
        def run(self):
                print ("I'm Starting the motor (in 3 seconds), I hope its calibrated and armed, if not stop the testing")
                time.sleep(3)
                print ("test started")

                # initiating the motor
                self.speed = self.MIN_VALUE
                self.pi.set_servo_pulsewidth(ESC, self.speed)
                print ("speed = %d for 3 seconds" % self.speed)
                time.sleep(3)

                # loop for increasing the speed
                while self.speed < self.MAX_VALUE and self.not_exited:
                        self.speed += 1
                        self.pi.set_servo_pulsewidth(ESC, self.speed)

                        if self.speed % 100 == 0:
                                print ("speed = %d for 3 seconds" % self.speed)
                                time.sleep(3)
                        else:
                                time.sleep(0.03)
                
                
                
                while self.speed > self.MIN_VALUE and self.not_exited:
                        self.speed -= 1
                        self.pi.set_servo_pulsewidth(ESC, self.speed)
                        
                        if self.speed % 100 == 0:
                                print ("speed = %d for 3 seconds" % self.speed)
                                time.sleep(3)
                        else:
                                time.sleep(0.03)
        
                self.speed = 0
                self.pi.set_servo_pulsewidth(ESC, self.speed)
                self.pi.stop()
                print("i am running")
        def stop(self):
                print("Stopping\n")
                self.not_exited = False
        
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

def destroy_test():
        file.close()
        esc_control_thread.stop()
        GPIO.cleanup
        top.destroy()

def stop_test():
        file.close()
        esc_control_thread.stop()

def test():
        global top
        global file
        global esc_control_thread
        top = Toplevel()
        top.title('Test')

        # Setting a wait button
        var = IntVar()
        i = 0
        button = Button(top, text="Start", command=lambda: var.set(i), font = desired_font)
        i = 0
        button = Button(top, text="Start", command=lambda: var.set(i), font = desired_font)
        button.pack()

        stop_button = Button(top, text="Stop", font = desired_font)
        stop_button.pack()

        destroy_button = Button(top, text="close window", font = desired_font)
        destroy_button.pack()

        MODES = [
                ("Data Collection Test (0% to 100%)", "DataCollection"),
                ("Pulse Test (40% to 80%) 30 min", "Pulse"),
                ("Constant Test (50% Test) 30 min", "Fifty"),
                ("Constant Test (100% Test) 10 min", "Hundred"),
        ]

        selected_mode = StringVar()
        selected_mode.set("DataCollection")

        for text, choice in MODES:
	        Radiobutton(top, text=text, variable=selected_mode, value=choice, font = desired_font).pack(anchor=W)

        while True:
                #Waiting for test selection
                i+=1
                button.wait_variable(var)

                file_path = "/home/pi/{}_ptr_with_gui.csv".format(datetime.now().strftime('%Y-%m-%d'))
                file = open(file_path, "a")
                i = 0
                j = 0
                test_label = "NA"
                if os.stat(file_path).st_size == 0:
                        file.write("timestamp,amb_temp,obj_temp,thrust,voltage,current,power,rpm,pwm,test_label\n")
                
                class UserExit(Exception):
                        pass

                print("WARNING- This project was made by Priyansh so anything can go wrong anytime")
                print("press ctrl+c to stop this program along with the motor")

                # starting the test
                esc_control_thread = data_collection.DataCollection(ESC)
                esc_control_thread.speed = 0
                esc_control_thread.start()

                destroy_button.config(command=destroy_test)
                stop_button.config(command=stop_test)

                while top.winfo_exists() == TRUE and esc_control_thread.is_alive() == TRUE and file.closed == False:
                        try:
                                i=i+1
                                now = datetime.now()
                                # ADC_Value = ADC.ADS1256_GetAll()
                                file.write(str(now)+","+str('sensor.get_ambient()')+","+str('sensor.get_object_1()')+","+str('hx.get_weight(5)')+","+str('0.00125*swapper(bus.read_word_data(0x41, 0x02))')+","+str('164.0*swapper(bus.read_word_data(0x41, 0x04))/32768.0')+","+str('25.0*164.0*swapper(bus.read_word_data(0x41, 0x03))/32768.0')+","+str('rpm')+","+str(esc_control_thread.speed)+","+test_label+"\n")
                                file.flush()
                                top.update()
                                time.sleep(0.05)
                
                        except (KeyboardInterrupt, SystemExit, UserExit):
                                file.close()
                                esc_control_thread.stop()
                                GPIO.cleanup
                                print ("stopping esc/motor and datalogging")
                                exit()
                file.close()


cal_button = Button(root, text="Calibrate", command=calibration, font = desired_font).pack()
manual_button = Button(root, text="Manual Control", command=control, font = desired_font).pack()
test_button = Button(root, text="Test (Datalogging)", command=test, font = desired_font).pack()
destroy_root_button = Button(root, text="close window", command=root.destroy, font = desired_font).pack()

root.protocol("WM_DELETE_WINDOW", disable)

mainloop()