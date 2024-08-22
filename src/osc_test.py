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

from pythonosc import osc_bundle_builder
from pythonosc import osc_message_builder

class OscSender():
    def __init__(self):
        self.config = DynamicConfigIni()
        print(self.config.DEFAULT.test)
        self.oscclient = pythonosc.udp_client.SimpleUDPClient(self.config.osc.addr, int(self.config.osc.port))
    
    def send(self):
        self.oscclient.send_message("/moreheat/test", random.random())

    def beatloop(self):
        print('beat')

    def build_bundle(self):
        bundle = osc_bundle_builder.OscBundleBuilder(
        osc_bundle_builder.IMMEDIATELY)
        
        msg1 = osc_message_builder.OscMessageBuilder(address="/moreheat/bundle/m1")
        msg1.add_arg(4.0)

        msg2 = osc_message_builder.OscMessageBuilder(address="/moreheat/bundle/m2")
        msg2.add_arg(20.0)

        bundle.add_content(msg1.build())
        bundle.add_content(msg2.build())

        bundle = bundle.build()
        self.oscclient.send(bundle)

if __name__ == "__main__":
    
    sender = OscSender()

    for x in range(10):
        sender.send()
        sender.build_bundle()
        time.sleep(1)
