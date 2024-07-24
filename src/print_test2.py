import StarTSPImage
from PIL import Image, ImageDraw

image = Image.new('RGB', (500, 500), color='White')
draw = ImageDraw.Draw(image)

something = 480
while something > 300:
    draw.ellipse((490 - something, 490 - something, something, something), fill='White')
    draw.ellipse((500 - something, 500- something, something - 10, something -10), fill='Red')
    something = something - 20

raster = StarTSPImage.imageToRaster(image, cut=False)

printer = open('/dev/usb/lp0', "wb")
printer.write(raster)
