import motor_control.standard_test
import motor_control.fifty_percent
import motor_control.hundred_percent
import sensors_and_data.datalogging as datalogging
import sensors_and_data.sensors as sensors

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
        
        sensor_control = sensors.Sensors()
        sensor_control.sensors_start()

        while test_toplevel.winfo_exists() == TRUE:
                
                #Waiting for test selection
                i+=1
                button.wait_variable(var)

                name = selected_mode.get()
                datalog = datalogging.Datalog()
                datalog.make_logfile(name)
                print(name)

                if name == "DataCollection":
                        esc_control_thread = motor_control.standard_test.StandardTest(ESC)
                elif name == "Pulse":
                        esc_control_thread = motor_control.standard_test.StandardTest(ESC)
                elif name == "Fifty":
                        esc_control_thread = motor_control.fifty_percent.Fifty(ESC)
                elif name == "Hundred":
                        esc_control_thread = motor_control.hundred_percent.Hundred(ESC)

                i = 0
                print("WARNING- This project was made by Priyansh so anything can go wrong anytime")
                print("press ctrl+c to stop this program along with the motor")

                esc_control_thread.speed = 0
                esc_control_thread.start()

                destroy_button.config(command=destroy_test)
                stop_button.config(command=stop_test)

                while test_toplevel.winfo_exists() == TRUE and esc_control_thread.is_alive() == TRUE:
                        try:
                                i=i+1
                                now = datetime.now()
                                sensor_control.sensors_data()
                                # ADC_Value = ADC.ADS1256_GetAll()
                                data = {}
                                data["timestamp"] = str(now)
                                data["amb_temp"] = 'sensor.get_ambient()'
                                data["obj_temp"] = "sensor.get_object_1()"
                                data["thrust"] = 'hx.get_weight(5)'
                                data["voltage"] = sensor_control.voltage
                                data["current"] = sensor_control.current
                                data["power"] = sensor_control.power
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
