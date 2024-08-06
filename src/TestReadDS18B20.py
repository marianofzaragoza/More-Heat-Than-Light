from config import DynamicConfigIni
import os
import time

config = DynamicConfigIni()
print(config.DEFAULT.test)



def read_temperature(sensor_id):
    base_dir = "/sys/bus/w1/devices/"
    device_folder = os.path.join(base_dir, sensor_id)
    device_file = os.path.join(device_folder, "w1_slave")

    with open(device_file, "r") as f:
        lines = f.readlines()
    
    if lines[0].strip().endswith("YES"):
        equals_pos = lines[1].find("t=")
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c
    return None

sensor_id = "28-00000f7650d5"
temperature = read_temperature(sensor_id)

def print_temperature(temperature):
    if temperature is not None:
        print(f"{temperature:.2f}°C")
    else:
        print("Failed to read the temperature.")

totalcicles = 121

#A los 61 apago
while totalcicles > 0: 
    print(str(121 - totalcicles))
    temperature = read_temperature("28-00000f7650d5")
    print(f"{temperature:.2f}°C")
    time.sleep(10)
    totalcicles = totalcicles - 1

print("termino")
    
