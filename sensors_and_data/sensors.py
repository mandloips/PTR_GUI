from smbus2 import SMBus
import RPi.GPIO as GPIO
from hx711 import HX711
from mlx90614 import MLX90614

class Sensors():

    def swapper(self, num):
        # for swapping the first and second byte
        p1 = 0
        p2 = 8
        n = 8
        shift1 = 0
        shift2 = 0
        value1 = 0
        value2 = 0
 
        while(n > 0):
       
            shift1 = 1 << p1

            shift2 = 1 << p2

            value1 = ((num & shift1))
            value2 = ((num & shift2))

            if((value1 == 0 and value2 != 0) or (value2 == 0 and value1 != 0)):
            
                if(value1 != 0):
                    num = num & (~shift1)
                    num = num | shift2

                else:
                    num = num & (~shift2)
                    num = num | shift1

            p1 += 1
            p2 += 1
            n -= 1

        return num
    
    def power_module(self):
        global bus
        bus = SMBus(1)

        INA226_CONST = 0.00512
        INA226_SHUNT = 0.0005
        _max_current = 164.0
        DN_MAX = 32768.0
        _rshunt = INA226_SHUNT
        _current_lsb = _max_current / DN_MAX
        _cal = INA226_CONST / (_current_lsb * _rshunt)

        bus.write_word_data(0x41, 0x00, self.swapper(int(DN_MAX)))
        bus.write_word_data(0x41, 0x05, self.swapper(int(_cal)))
    
    def hx711_module(self):
        hx = HX711(23, 24)
        hx.set_reading_format("MSB", "MSB")
        hx.set_reference_unit(231.924882629108)
        hx.reset()
        hx.tare()
        print("Tare done! (for load cell)")
    
    def sensors_start(self):
        self.power_module()

    def sensors_data(self):
        self.voltage = 0.00125*self.swapper(bus.read_word_data(0x41, 0x02))
        self.current = 164.0*self.swapper(bus.read_word_data(0x41, 0x04))/32768.0
        self.power = 25.0*164.0*self.swapper(bus.read_word_data(0x41, 0x03))/32768.0

