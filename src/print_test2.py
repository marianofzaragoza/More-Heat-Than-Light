import StarTSPImage
from PIL import Image, ImageDraw
import time


image = Image.new('RGB', (500, 1000), color='White')

draw = ImageDraw.Draw(image)
draw.line([(10, 0), (10, 999)], fill="black", width=2)
raster = StarTSPImage.imageToRaster(image, cut=False)
printer = open('/dev/usb/lp0', "wb")
printer.write(raster) 
printer.close()

