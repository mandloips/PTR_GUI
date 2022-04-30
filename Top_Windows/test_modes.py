import Motor_Control.data_collection
from tkinter import *
from tkinter import font
from datetime import datetime
import os
import time
import RPi.GPIO as GPIO


def destroy_test():
        file.close()
        esc_control_thread.stop()
        GPIO.cleanup
        test_toplevel.destroy()

def stop_test():
        file.close()
        esc_control_thread.stop()

def test(ESC):
        global test_toplevel
        global file
        global esc_control_thread
        desired_font = font.Font(size = 25)

        test_toplevel = Toplevel()
        test_toplevel.title('Test')

        test_toplevel.grab_set()

        # Setting a wait button
        var = IntVar()
        i = 0
        button = Button(test_toplevel, text="Start", command=lambda: var.set(i), font = desired_font)
        i = 0
        button = Button(test_toplevel, text="Start", command=lambda: var.set(i), font = desired_font)
        button.pack()

        stop_button = Button(test_toplevel, text="Stop", font = desired_font)
        stop_button.pack()

        destroy_button = Button(test_toplevel, text="close window", command=test_toplevel.destroy, font = desired_font)
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
	        Radiobutton(test_toplevel, text=text, variable=selected_mode, value=choice, font = desired_font).pack(anchor=W)

        while test_toplevel.winfo_exists() == TRUE:
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
                

                esc_control_thread = Motor_Control.data_collection.DataCollection(ESC)
                esc_control_thread.speed = 0
                esc_control_thread.start()
                destroy_button.config(command=destroy_test)
                stop_button.config(command=stop_test)

                while test_toplevel.winfo_exists() == TRUE and esc_control_thread.is_alive() == TRUE and file.closed == False:
                        try:
                                i=i+1
                                now = datetime.now()
                                # ADC_Value = ADC.ADS1256_GetAll()
                                file.write(str(now)+","+str('sensor.get_ambient()')+","+str('sensor.get_object_1()')+","+str('hx.get_weight(5)')+","+str('0.00125*swapper(bus.read_word_data(0x41, 0x02))')+","+str('164.0*swapper(bus.read_word_data(0x41, 0x04))/32768.0')+","+str('25.0*164.0*swapper(bus.read_word_data(0x41, 0x03))/32768.0')+","+str('rpm')+","+str(esc_control_thread.speed)+","+test_label+"\n")
                                file.flush()
                                test_toplevel.update()
                                time.sleep(0.05)
                
                        except (KeyboardInterrupt, SystemExit, UserExit):
                                file.close()
                                esc_control_thread.stop()
                                GPIO.cleanup
                                print ("stopping esc/motor and datalogging")
                                break
                file.close()