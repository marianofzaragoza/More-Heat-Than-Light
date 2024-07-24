import StarTSPImage
from PIL import Image, ImageDraw


image = Image.new('RGB', (500, 10000), color='White')

draw = ImageDraw.Draw(image)
draw.line((0, 0, 500, 10000), fill='Black', width=3)



raster = StarTSPImage.imageToRaster(image, cut=False)

printer = open('/dev/usb/lp0', "wb")
printer.write(raster)
