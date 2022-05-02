import time
import Motor_Control.esc_control_thread

#ESC Control Thread
class Hundred(Motor_Control.esc_control_thread.ESCControlThread):

    def run(self):
        self.starting()
        start_time = time.time()
        total_run_time = 60
        end_time = start_time + total_run_time
        # loop for increasing the speed
        while self.speed < self.MAX_VALUE and time.time() < end_time and self.not_exited:
            self.speed += 1
            self.pi.set_servo_pulsewidth(self.esc, self.speed)
            print ("speed = %d for 0.05 seconds" % self.speed)
            run_time = time.time() - start_time
            print("runtime = %f" % run_time)
            time.sleep(0.03)
        
        while time.time() < end_time and self.not_exited:
            run_time = time.time() - start_time
            print("runtime = %f" % run_time)
            time.sleep(1)

    
        self.speed = 0
        self.pi.set_servo_pulsewidth(self.esc, self.speed)
        self.pi.stop()
        print("i am running")