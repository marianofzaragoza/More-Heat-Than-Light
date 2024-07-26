import StarTSPImage
from PIL import Image, ImageDraw
import time
import random

def image_temperatures(a_temp, b_temp):
    # Create a 500x10 image with a white background
    image = Image.new('RGB', (500, 10), color='White')
    draw = ImageDraw.Draw(image)
    draw.line((a_temp*10, 0, a_temp*10, 10), fill='Black', width=3) 
    draw.line((b_temp*10, 0, b_temp*10, 10), fill='Black', width=3)  
    return image

def print_image(a_temp, b_temp, entanglement, broken_channel):
    if entanglement:
        #entanglement image
        image = Image.open("/home/agustina/More-Heat-Than-Light/src/single_photon.png")
    elif broken_channel:
        #brokenn_Channel image
        image = Image.open("/home/agustina/More-Heat-Than-Light/src/broken_channel.png")
    else:
        image = image_temperatures(a_temp, b_temp)
    #printer driver
    raster = StarTSPImage.imageToRaster(image, cut=False)
    printer = open('/dev/usb/lp0', "wb")
    printer.write(raster)  
    printer.close()


#Testing script
dontrepeat = False
a=9
b=9
while True:
    #sure they dont go out of range

    a = max(0, min(a, 499))
    b = max(0, min(b, 499))

    if a < 10 and b < 10 and a==b and dontrepeat == False:
        print_image(a, b, True, False)
        dontrepeat = True
        
    elif abs(a-b)>10 and dontrepeat == False:
        print_image(a, b, False, True)
        dontrepeat = True

    else :
        print_image(a, b, False, False)
        if not (a < 10 and b < 10 and a==b) and not(abs(a-b)>10):
            dontrepeat = False
    a = a + random.randint(-1, 1)
    b = b + random.randint(-1, 1)

