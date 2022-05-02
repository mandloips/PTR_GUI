import Motor_Control.data_collection
import Motor_Control.fifty_percent
import Motor_Control.hundred_percent
from tkinter import *
from tkinter import font
from datetime import datetime
import os
import time
import RPi.GPIO as GPIO
import logging
import csv
import io
from pathlib import Path
class CSVFormatter(logging.Formatter):
	def __init__(self):
		super().__init__()
	def format(self, record):
		stringIO = io.StringIO()
		writer = csv.writer(stringIO, quoting=csv.QUOTE_ALL)
		writer.writerow(record.msg)
		record.msg = stringIO.getvalue().strip()
		return super().format(record)

def destroy_test():
        esc_control_thread.stop()
        GPIO.cleanup
        test_toplevel.destroy()

def stop_test():
        esc_control_thread.stop()

def test(ESC, font_size):
        FILE = Path(__file__).resolve()
        ROOT = FILE.parents[0]
        ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

        save_dir = ROOT / 'logs'
        if not os.path.isdir(save_dir):
                os.mkdir(save_dir)

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

                file_name="Test_Logs-"+str(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))+'.csv'
                logging.basicConfig(filename=save_dir / file_name,format=' %(message)s', level=logging.DEBUG)
                logger = logging.getLogger(__name__)
                logger.info("timestamp,amb_temp,obj_temp,thrust,voltage,current,power,rpm,pwm,test_label")
                test_label = "NA"

                i = 0
                j = 0
                class UserExit(Exception):
                        pass
                print("WARNING- This project was made by Priyansh so anything can go wrong anytime")
                print("press ctrl+c to stop this program along with the motor")

                esc_control_thread = Motor_Control.hundred_percent.Hundred(ESC)
                esc_control_thread.speed = 0
                esc_control_thread.start()
                destroy_button.config(command=destroy_test)
                stop_button.config(command=stop_test)
                while test_toplevel.winfo_exists() == TRUE and esc_control_thread.is_alive() == TRUE:
                        try:
                                i=i+1
                                now = datetime.now()
                                # ADC_Value = ADC.ADS1256_GetAll()
                                logger.info(str(now)+","+str('sensor.get_ambient()')+","+str('sensor.get_object_1()')
                                +","+str('hx.get_weight(5)')+","+str('0.00125*swapper(bus.read_word_data(0x41, 0x02))')
                                +","+str('164.0*swapper(bus.read_word_data(0x41, 0x04))/32768.0')+","
                                +str('25.0*164.0*swapper(bus.read_word_data(0x41, 0x03))/32768.0')+","+str('rpm')+","
                                +str(esc_control_thread.speed)+","+test_label+"\n")
                                test_toplevel.update()
                                time.sleep(0.05)

                        except (KeyboardInterrupt, SystemExit, UserExit):
                                esc_control_thread.stop()
                                GPIO.cleanup
                                print ("stopping esc/motor and datalogging")
                                break
