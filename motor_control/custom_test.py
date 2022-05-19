import threading
import pigpio
import time
import motor_control.esc_control_thread

#ESC Control Thread
class CustomTest(threading.Thread):
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
    
    def run(self):
        self.starting()
        
        while self.not_exited:

            while self.speed < self.MIN_VALUE + 80*10 and self.not_exited:
                self.speed += 100
                self.pi.set_servo_pulsewidth(self.esc, self.speed)
                print ("speed = %d for 5 seconds\n" % self.speed)
                time.sleep(5)

            while self.speed > self.MIN_VALUE + 40*10 and self.not_exited:
                self.speed -= 100
                self.pi.set_servo_pulsewidth(self.esc, self.speed)
                print ("speed = %d for 5 seconds\n" % self.speed)
                time.sleep(5)

        if self.not_exited:
            self.speed = 0
            self.pi.set_servo_pulsewidth(self.esc, self.speed)
            self.pi.stop()
            print("pulse ka stop ran")

    def stop(self):
        if self.not_exited:
            print("Stopping esc control thread\n")
            self.not_exited = False
            self.speed = 0
            self.pi.set_servo_pulsewidth(self.esc, self.speed)
            self.pi.stop()
