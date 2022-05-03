import time
import motor_control.esc_control_thread

#ESC Control Thread
class Fifty(motor_control.esc_control_thread.ESCControlThread):

    def run(self):
        self.starting()
        # loop for increasing the speed
        while self.speed < self.MIN_VALUE + 50*10 and self.not_exited:
            self.speed += 1
            print(self.speed)
            self.pi.set_servo_pulsewidth(self.esc, self.speed)
            print ("speed = %d for 3 seconds" % self.speed)
            time.sleep(0.05)
        
        while self.not_exited:
            time.sleep(1)
    
        self.speed = 0
        self.pi.set_servo_pulsewidth(self.esc, self.speed)
        self.pi.stop()
        print("i am running")