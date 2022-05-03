import motor_control.data_collection
import motor_control.fifty_percent
import motor_control.hundred_percent
import sensors_and_data.datalogging as datalogging
from tkinter import *
from tkinter import font
from datetime import datetime
import time
import RPi.GPIO as GPIO

def destroy_test():
        esc_control_thread.stop()
        GPIO.cleanup
        test_toplevel.destroy()

def stop_test():
        esc_control_thread.stop()

def test(ESC, font_size):

        global test_toplevel
        global file
        global esc_control_thread
        desired_font = font.Font(size = font_size)

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

                name = selected_mode.get()
                datalog = datalogging.Datalog()
                datalog.make_logfile(name)
                print(name)

                i = 0
                print("WARNING- This project was made by Priyansh so anything can go wrong anytime")
                print("press ctrl+c to stop this program along with the motor")

                esc_control_thread = motor_control.hundred_percent.Hundred(ESC)
                esc_control_thread.speed = 0
                esc_control_thread.start()

                destroy_button.config(command=destroy_test)
                stop_button.config(command=stop_test)

                while test_toplevel.winfo_exists() == TRUE and esc_control_thread.is_alive() == TRUE:
                        try:
                                i=i+1
                                now = datetime.now()
                                # ADC_Value = ADC.ADS1256_GetAll()
                                data = {}
                                data["timestamp"] = str(now)
                                data["amb_temp"] = 'sensor.get_ambient()'
                                data["obj_temp"] = "sensor.get_object_1()"
                                data["thrust"] = 'hx.get_weight(5)'
                                data["voltage"] = '0.00125*swapper(bus.read_word_data(0x41, 0x02))'
                                data["current"] = '164.0*swapper(bus.read_word_data(0x41, 0x04))/32768.0'
                                data["power"] = '25.0*164.0*swapper(bus.read_word_data(0x41, 0x03))/32768.0'
                                data["rpm"] = 'rpm'
                                data["pwm"] = esc_control_thread.speed
                                print(data)

                                datalog.log_data(data)
                                
                                test_toplevel.update()
                                time.sleep(0.05)

                        except (KeyboardInterrupt, SystemExit):
                                esc_control_thread.stop()
                                GPIO.cleanup
                                print ("stopping esc/motor and datalogging")
                                break
