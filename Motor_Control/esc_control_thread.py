import threading
import pigpio
import time

#ESC Control Thread
class ESCControlThread(threading.Thread):
    MAX_VALUE = 2000        # if you are changing here then change for calibration too
    MIN_VALUE = 1000        # if you are changing here then change for calibration too
    
    def __init__(self, esc):
        threading.Thread.__init__(self)
        self.not_exited = True
        self.esc = esc
        self.speed = 0
        self.pi = pigpio.pi();
        self.pi.set_servo_pulsewidth(self.esc, self.speed)

    def starting(self):
        print ("I'm Starting the motor (in 3 seconds), I hope its calibrated and armed, if not stop the testing")
        time.sleep(3)
        print ("test started")

        # initiating the motor
        self.speed = self.MIN_VALUE
        self.pi.set_servo_pulsewidth(self.esc, self.speed)
        print ("speed = %d for 3 seconds" % self.speed)
        time.sleep(3)

    def stop(self):
        print("Stopping\n")
        self.not_exited = False
