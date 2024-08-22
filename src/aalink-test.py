import asyncio
from PIL import Image, ImageDraw
from aalink import Link
import time
import StarTSPImage

async def main():
    loop = asyncio.get_running_loop()

    link = Link(60, loop)
    await asyncio.sleep(0.5)

    link.enabled = True
    #link.quantum = 4
    print(dir(link))
 
    while True:
        await link.sync(3)
        print('bang!')
        #time.sleep(0)
        img = Image.new('RGB', (576, 1), "white")

        raster = StarTSPImage.imageToRaster(img, cut=False)
        printer = open('/dev/usb/lp0', "wb")
        printer.write(raster) 
        printer.close()
        
        print(link.tempo)


asyncio.run(main())


#['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'beat', 'enabled', 'force_beat', 'num_peers', 'phase', 'playing', 'quantum', 'request_beat', 'request_beat_at_start_playing_time', 'set_is_playing_and_request_beat_at_time', 'set_num_peers_callback', 'set_start_stop_callback', 'set_tempo_callback', 'start_stop_sync_enabled', 'sync', 'tempo', 'time']

