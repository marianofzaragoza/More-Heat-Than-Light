from config import DynamicConfigIni
import os
import time

config = DynamicConfigIni()
print(config.DEFAULT.test)

class Thermometer():
    def __init__(self):
        self.config = DynamicConfigIni()
        self.nodename = self.config.DEFAULT.nodename  # Access the nodename correctly
        self.weight_of_outside_thermometer = self.config.thermometer.weight_of_outside_thermometer
        self.sensor_id_out = getattr(self.config, self.nodename).thermometer_out_id  # Access the sensor ID for the specified node
        self.sensor_id_radiator = getattr(self.config, self.nodename).thermometer_radiator_id  # Access the sensor ID for the radiator

    def read_one_temperature(self, sensor_id):
        base_dir = "/sys/bus/w1/devices/"
        device_folder = os.path.join(base_dir, sensor_id)
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
        out = float(self.read_one_temperature(self.sensor_id_out))*float(self.weight_of_outside_thermometer)
        radiator = float(self.read_one_temperature(self.sensor_id_radiator))*(1-float(self.weight_of_outside_thermometer))
        return round(out + radiator, 2)

    def test(self):
        #print for a minute
        for i in range(60):
            time.sleep(1)
            temperature_out = self.read_one_temperature(self.sensor_id_out)
            temperature_radiator = self.read_one_temperature(self.sensor_id_radiator)
            temperature_avarage = self.read_total_temperature()
            print(f"OUT:{temperature_out}")
            print(f"RADIATOR:{temperature_radiator}")
            print(f"WEIGHTED AVARAGE:{temperature_avarage}")


if __name__ == "__main__":
    thermometer = Thermometer()
    thermometer.test()

    
