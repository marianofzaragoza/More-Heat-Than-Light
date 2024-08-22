from config import DynamicConfigIni
import os
import time
import random
config = DynamicConfigIni()
print(config.DEFAULT.test)

class Thermometer():
    def __init__(self, testing=False):
        self.testing = testing
        self.config = DynamicConfigIni()
        self.nodename = self.config.DEFAULT.nodename  # Access the nodename
        self.tempstep = float(self.config.DEFAULT.tempstep)
        self.last_temp_outside = 20
        self.last_temp_radiator = 20
        self.tick = 0

        self.weight_of_outside_thermometer = self.config.thermometer.weight_of_outside_thermometer 

        self.sensor_id_out = getattr(self.config, self.nodename).thermometer_out_id  # sensor_id of radiator
        self.sensor_id_radiator = getattr(self.config, self.nodename).thermometer_radiator_id  # sensor_id of outside

    def gen_test_temperature(self):
        return 23.0

    def read_one_temperature(self, sensor_id):
        if self.testing:
            return self.gen_test_temperature()
        else:
            basedir = "/sys/bus/w1/devices/"
            device_folder = os.path.join(basedir, sensor_id)
            device_file = os.path.join(device_folder, "w1_slave")

            with open(device_file, "r") as f:
                lines = f.readlines()
            
            if lines[0].strip().endswith("YES"):
                equals_pos = lines[1].find("t=")
                if equals_pos != -1:
                    temp_string = lines[1][equals_pos + 2:]
                    temp_c = round(float(temp_string) / 1000.0, 2)
                    return temp_c
        return None

    #this is the important 
    def read_total_temperature(self):
        if not self.testing:
            self.last_temp_outside = float(self.read_one_temperature(self.sensor_id_out))*float(self.weight_of_outside_thermometer) 
            self.last_temp_radiator = float(self.read_one_temperature(self.sensor_id_radiator))*(1-float(self.weight_of_outside_thermometer))
        else:
            step = self.tempstep
            if self.last_temp_outside > 30:
                self.last_temp_outside = self.last_temp_outside + random.uniform(-step, step)
            elif self.last_temp_outside < -10:
                self.last_temp_outside = self.last_temp_outside + random.uniform(0, step) 
            else:
                self.last_temp_outside = self.last_temp_outside + random.uniform(-step, step)
             
            if self.last_temp_radiator > 30:
                self.last_temp_radiator = self.last_temp_radiator + random.uniform(-step, step)
            elif self.last_temp_radiator < -10:
                self.last_temp_radiator = self.last_temp_radiator + random.uniform(0, step) 
            else:
                self.last_temp_radiator = self.last_temp_radiator + random.uniform(-step, step)
            

            #self.last_temp_radiator = self.last_temp_outside + random.uniform(-2.0, 2.0)
        return round(self.last_temp_outside + self.last_temp_radiator, 2)

    def test(self):
        #print for a minute
        for i in range(60):
            temperature_out = self.read_one_temperature(self.sensor_id_out)
            temperature_radiator = self.read_one_temperature(self.sensor_id_radiator)
            temperature_avarage = self.read_total_temperature()
            print(f"OUT:{temperature_out}")
            print(f"RADIATOR:{temperature_radiator}")
            print(f"WEIGHTED AVARAGE:{temperature_avarage}")


if __name__ == "__main__":
    thermometer = Thermometer(testing=True)
    thermometer.test()

    
