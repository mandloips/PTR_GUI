import time
import threading
import pigpio
import Motor_Control.esc_control_thread

#ESC Control Thread
class DataCollection(Motor_Control.esc_control_thread.ESCControlThread):

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