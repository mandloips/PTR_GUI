import motor_control.standard_test
import motor_control.fifty_percent
import motor_control.hundred_percent
import motor_control.pulse_test

import sensors_and_data.datalogging as datalogging
import sensors_and_data.sensors as sensors

from tkinter import *
from tkinter import font
from datetime import datetime
import time
import RPi.GPIO as GPIO

def destroy_test():
    esc_control.stop()
    GPIO.cleanup
    test_toplevel.destroy()

def stop_test():
    esc_control.stop()

def test_description(name):
    if name == "Standard":
        descriptionlabel.config(text = "This test goes from 0% to 100% [gradually] while stopping for 3 sec after every 10%")
    elif name == "Pulse":
        descriptionlabel.config(text = "This test goes from 40% to 80% with sudden 10% [increase] and [decrease]")
    elif name == "Fifty":
        descriptionlabel.config(text = "This test goes from 0% to 50% [gradually] and then remains constant at 50%")
    elif name == "Hundred":
        descriptionlabel.config(text = "This test goes from 0% to 100% [gradually] and then remains constant at 100%")
    else:
        descriptionlabel.config(text = "NA")

def test(ESC, font_size):

    global test_toplevel
    global esc_control
    global descriptionlabel
    desired_font = font.Font(size = font_size)

    test_toplevel = Toplevel()
    test_toplevel.title('Test')
    test_toplevel.attributes('-fullscreen', True)


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
        ("Standard Test (0% to 100%)    2 min", "Standard"),
        ("Pulse Test (40% to 80%)       30 min", "Pulse"),
        ("Constant Test (50% Test)      30 min", "Fifty"),
        ("Constant Test (100% Test)     10 min", "Hundred"),
    ]

    selected_mode = StringVar()
    selected_mode.set("DataCollection")

    for text, choice in MODES:
        Radiobutton(test_toplevel, text=text, variable=selected_mode, value=choice, font = desired_font, borderwidth=5, command=lambda: test_description(selected_mode.get())).pack(anchor=W)

    descriptionlabel = Label(test_toplevel, text="test description: NA")
    descriptionlabel.pack()

    test_toplevel.update()

    sensor_control = sensors.Sensors()
    sensor_control.sensors_start()
    datalog = datalogging.Datalog()

    while test_toplevel.winfo_exists() == TRUE:
            
        #Waiting for test selection
        i+=1
        button.wait_variable(var)

        name = selected_mode.get()
        datalog.make_logfile(name)
        print(name)

        if name == "Standard":
            esc_control = motor_control.standard_test.StandardTest(ESC)
            total_run_time = 5*60
        elif name == "Pulse":
            esc_control = motor_control.pulse_test.PulseTest(ESC)
            total_run_time = 30*60
        elif name == "Fifty":
            esc_control = motor_control.fifty_percent.Fifty(ESC)
            total_run_time = 30*60
        elif name == "Hundred":
            esc_control = motor_control.hundred_percent.Hundred(ESC)
            total_run_time = 5*60
        else:
            esc_control = motor_control.standard_test.StandardTest(ESC)
            total_run_time = 60

        i = 0

        esc_control.speed = 0
        esc_control.start()

        destroy_button.config(command=destroy_test)
        stop_button.config(command=stop_test)

        start_time = time.time()
        end_time = start_time + total_run_time

        class TempHigh(Exception):
            pass

        class VoltageLow(Exception):
            pass

        while test_toplevel.winfo_exists() == TRUE and esc_control.is_alive() == TRUE and time.time() < end_time:
            try:
                i=i+1
                now = datetime.now()
                sensor_control.sensors_data()
                # ADC_Value = ADC.ADS1256_GetAll()
                data = sensor_control.data
                data["pwm"] = esc_control.speed
                data["run_time"] = time.time() - start_time
                print(data)

                datalog.log_data(data)
                if data["esc_temp"] > 80:
                        raise TempHigh()
                elif data["voltage"] < 21:
                        raise VoltageLow()
                
                print("printed")
                
                test_toplevel.update()
                time.sleep(0.05)

            except TempHigh:
                esc_control.stop()
                print ("high temperature alert")
                break
            
            except VoltageLow:
                esc_control.stop()
                print ("battery drain alert")
                break

            except (KeyboardInterrupt, SystemExit):
                esc_control.stop()
                print ("stopping esc/motor and datalogging")
                break
        esc_control.stop()