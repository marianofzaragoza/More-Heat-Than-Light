from config import DynamicConfigIni
import logging
import mhlog
import os
import time
import random
import mhlog


class Thermometer():
    def __init__(self, testing=False):

        logging.setLoggerClass(mhlog.Logger)
        self.log = mhlog.getLog("thermomether", self)

        assert isinstance(self.log, mhlog.Logger)
        self.log.setLevel(logging.INFO)

        self.testing = testing
        self.config = DynamicConfigIni()
        self.nodename = self.config.DEFAULT.nodename  # Access the nodename
        try:
            self.tempstep = float(self.config.DEFAULT.tempstep)
        except AttributeError as e:
            self.log.critical(e)
        self.last_temp_outside = 20
        self.last_temp_radiator = 20
        self.tick = 0

        self.weight_of_outside_thermometer = self.config.thermometer.weight_of_outside_thermometer 
        
        if not testing:
            self.sensor_id_out = getattr(self.config, self.nodename).thermometer_out_id  # sensor_id of radiator
            self.sensor_id_radiator = getattr(self.config, self.nodename).thermometer_radiator_id  # sensor_id of outside
        else:
            self.sensor_id_out = False
            self.sensor_id_radiator = False



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
                #print(lines)
           
            try:
                if lines[0].strip().endswith("YES"):
                    equals_pos = lines[1].find("t=")
                    if equals_pos != -1:
                        temp_string = lines[1][equals_pos + 2:]
                        #temp_c = round(float(temp_string) / 1000.0, 2)
                        temp_c = float(temp_string) / 1000
                        #print("sensor: " + sensor_id + " temp_c= " + str(temp_c))
                        return temp_c

            #FIXME this should not happen, also should return last measurement
            except IndexError as e:
                self.log.critical("temp reading error " + str(e))
                return 0.0
        return None

    #this is the important 
    def read_total_temperature(self):
        if not self.testing:
            self.last_temp_outside = float(self.read_one_temperature(self.sensor_id_out))*float(self.weight_of_outside_thermometer) 
            self.last_temp_radiator = float(self.read_one_temperature(self.sensor_id_radiator))*(1-float(self.weight_of_outside_thermometer))
            #print("tem out: " + str(self.last_temp_outside) + "rad: " + str(self.last_temp_radiator))

            self.log.warning("temps: " + str(self.last_temp_outside) + ' ' + str(self.last_temp_radiator) + ' ' + str(round((self.last_temp_outside + self.last_temp_radiator) )))

            return (self.last_temp_outside + self.last_temp_radiator)

        else:
            step = self.tempstep
            if self.last_temp_outside > 30:
                self.last_temp_outside = self.last_temp_outside + random.uniform(-step, 0)
            elif self.last_temp_outside < -10:
                self.last_temp_outside = self.last_temp_outside + random.uniform(0, step) 
            else:
                self.last_temp_outside = self.last_temp_outside + random.uniform(-step, step)
             
            if self.last_temp_radiator > 80:
                self.last_temp_radiator = self.last_temp_radiator + random.uniform(-step, 0)
            elif self.last_temp_radiator <  20:
                self.last_temp_radiator = self.last_temp_radiator + random.uniform(0, step) 
            else:
                self.last_temp_radiator = self.last_temp_radiator + random.uniform(-step, step)
 
            #self.log.warning("too high" + str(-step) + ' ' + str(step) + ' ' + str(random.uniform( -1, 1)))
            self.log.warning("temps: " + str(self.last_temp_outside) + ' ' + str(self.last_temp_radiator) + ' ' + str(round((self.last_temp_outside + self.last_temp_radiator) / 2)))
           
            return (self.last_temp_outside + self.last_temp_radiator) / 2

    def test(self):
        #print for a minute
        for i in range(60):
            temperature_out = self.read_one_temperature(self.sensor_id_out)
            temperature_radiator = self.read_one_temperature(self.sensor_id_radiator)
            temperature_avarage = self.read_total_temperature()
            self.log.debug(f"OUT:{temperature_out}")
            self.log.debug(f"RADIATOR:{temperature_radiator}")
            self.log.debug(f"WEIGHTED AVARAGE:{temperature_avarage}")


if __name__ == "__main__":
    thermometer = Thermometer(testing=False)
    thermometer.test()

    
