import time
from PIL import Image, ImageDraw
import StarTSPImage
import os

sensor_id = "28-00000f7650d5"

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

def create_image(previous_temp):
    # Create a new 500x1 image
    image = Image.new('RGB', (500, 50), color='White')
    draw = ImageDraw.Draw(image)
    
    temperature = read_temperature(sensor_id)
    print(temperature)
    
    # Draw a point in the middle
    draw.line((int(previous_temp)*10, 0, int(temperature)*10, 50), fill='Black', width=3)

    return image, temperature

def print_image(image):
    # Convert the image to raster format
    raster = StarTSPImage.imageToRaster(image, cut=False)
    
    # Send the raster data to the printer
    with open('/dev/usb/lp0', "wb") as printer:
        printer.write(raster)



def main():

    previous_temp = read_temperature(sensor_id)

    while True:
        
        # Create the image
        image, previous_temp = create_image(previous_temp)
        
        # Print the image
        print_image(image)
        
        # Wait for 2 seconds
        time.sleep(0.1)

if __name__ == "__main__":
    main()
