import asyncio
from PIL import Image, ImageDraw
from aalink import Link
import time
import StarTSPImage

async def main():
    loop = asyncio.get_running_loop()

    link = Link(120, loop)
    await asyncio.sleep(0.5)

    link.enabled = True
    link.quantum = 4
    print(dir(link))
 
    while True:
        await link.sync(2)
        print('bang!')
        #time.sleep(0)
        img = Image.new('RGB', (576, 1), "white")

        raster = StarTSPImage.imageToRaster(img, cut=False)
        printer = open('/dev/usb/lp0', "wb")
        printer.write(raster) 
        printer.close()
        
        print(link.tempo)


asyncio.run(main())
