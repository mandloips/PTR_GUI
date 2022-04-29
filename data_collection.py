import time
import threading
import pigpio

#ESC Control Thread
class DataCollection(threading.Thread):
    MAX_VALUE = 1200        # if you are changing here then change for calibration too
    MIN_VALUE = 1000        # if you are changing here then change for calibration too
    speed = 0       
    
    def __init__(self, esc):
        threading.Thread.__init__(self)
        self.esc = esc
        self.speed = 0
        self.pi = pigpio.pi();
        self.pi.set_servo_pulsewidth(self.esc, self.speed)
        self.not_exited = True
    
    def run(self):
        print ("I'm Starting the motor (in 3 seconds), I hope its calibrated and armed, if not stop the testing")
        time.sleep(3)
        print ("test started")

        # initiating the motor
        self.speed = self.MIN_VALUE
        self.pi.set_servo_pulsewidth(self.esc, self.speed)
        print ("speed = %d for 3 seconds" % self.speed)
        time.sleep(3)

        # loop for increasing the speed
        while self.speed < self.MAX_VALUE and self.not_exited:
            self.speed += 1
            self.pi.set_servo_pulsewidth(self.esc, self.speed)

            if self.speed % 100 == 0:
                print ("speed = %d for 3 seconds" % self.speed)
                time.sleep(3)
            else:
                time.sleep(0.03)
        
        while self.speed > self.MIN_VALUE and self.not_exited:
            self.speed -= 1
            self.pi.set_servo_pulsewidth(self.esc, self.speed)
            
            if self.speed % 100 == 0:
                print ("speed = %d for 3 seconds" % self.speed)
                time.sleep(3)
            else:
                time.sleep(0.03)
    
            self.speed = 0
            self.pi.set_servo_pulsewidth(self.esc, self.speed)
            self.pi.stop()
            print("i am running")
    
    def stop(self):
        print("Stopping\n")
        self.not_exited = False
