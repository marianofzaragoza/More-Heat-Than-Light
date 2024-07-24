#!/usr/bin/env venv/bin/python3
import StarTSPImage
import usb.core
from PIL import Image, ImageDraw

vendorId = 0x0519   # Star
productId = 0x0003  # TSP143

dev = usb.core.find(idVendor=vendorId, idProduct=productId)

if dev:

    print('Found:', usb.util.get_string(dev, dev.iProduct))

    # Build PIL image
    image = Image.new('RGB', (500, 500), color='White')
    draw = ImageDraw.Draw(image)
    draw.ellipse((0, 0, 500, 500), fill='Black')
    draw.ellipse((10, 10, 490, 490), fill='White')

    # Create raster for Star
    raster = StarTSPImage.imageToRaster(image, cut=True)

    # Send to device using endpoint 2 (OUT)
    dev.write(2, raster)

else:
    print('Could not find device')
