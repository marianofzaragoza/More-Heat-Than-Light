"""Small example OSC client

This program sends 10 random values between 0.0 and 1.0 to the /filter address,
waiting for 1 seconds between each value.
"""
import argparse
import random
import time
from config import DynamicConfigIni

from pythonosc import udp_client

import pythonosc
import asyncio

from aalink import Link


class OscSender():
    def __init__(self):
        self.config = DynamicConfigIni()
        print(self.config.DEFAULT.test)
        self.oscclient = pythonosc.udp_client.SimpleUDPClient(self.config.osc.addr, int(self.config.osc.port))
    
    def send(self):
        self.oscclient.send_message("/moreheat/test", random.random())

    def beatloop(self):


if __name__ == "__main__":
    
    sender = OscSender()

    for x in range(10):
        sender.send()
        time.sleep(1)
