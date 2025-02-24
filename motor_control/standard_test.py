import time
import motor_control.esc_control_thread

#ESC Control Thread
class StandardTest(motor_control.esc_control_thread.ESCControlThread):

    def run(self):
        self.starting()
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
    
        if self.not_exited:
            self.speed = 0
            self.pi.set_servo_pulsewidth(self.esc, self.speed)
            self.pi.stop()