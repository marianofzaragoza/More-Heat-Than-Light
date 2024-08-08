import asyncio

from aalink import Link

async def main():
    loop = asyncio.get_running_loop()

    link = Link(120, loop)
    await asyncio.sleep(0.5)

    link.enabled = True
    link.quantum = 4
    print(dir(link))
 
    while True:
        await link.sync(1)
        print('bang!')
        print(link.tempo)

asyncio.run(main())
