import threading
import pigpio

#ESC Control Thread
class ESCControlThread(threading.Thread):
    MAX_VALUE = 2000        # if you are changing here then change for calibration too
    MIN_VALUE = 1000        # if you are changing here then change for calibration too
    
    def __init__(self, esc):
        threading.Thread.__init__(self)
        self.esc = esc
        self.speed = 0
        self.pi = pigpio.pi();
        self.pi.set_servo_pulsewidth(self.esc, self.speed)
        self.not_exited = True
    
    def stop(self):
        print("Stopping\n")
        self.not_exited = False
