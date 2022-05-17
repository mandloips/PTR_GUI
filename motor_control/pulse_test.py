import time
import motor_control.esc_control_thread

#ESC Control Thread
class PulseTest(motor_control.esc_control_thread.ESCControlThread):

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