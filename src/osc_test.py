"""
osc sender
"""
import argparse
import random
import time
from config import DynamicConfigIni
import logging
import mhlog 
import pathlib
from pythonosc import udp_client

import pythonosc
import asyncio

from aalink import Link

from pythonosc import osc_bundle_builder
from pythonosc import osc_message_builder

class OscSender():
    def __init__(self):
        logging.setLoggerClass(mhlog.Logger)
        self.log = mhlog.getLog("osc", self)
        self.log.setLevel(logging.WARN)
        srcdir = pathlib.Path(__file__).parent.resolve()
 
        self.config = DynamicConfigIni()
        self.log.info('hello from osc')
        self.oscclient = pythonosc.udp_client.SimpleUDPClient(self.config.osc.addr, int(self.config.osc.port))

    def send_video_msg(self,ps):
        self.log.info("send video msg")
        bundle = osc_bundle_builder.OscBundleBuilder(osc_bundle_builder.IMMEDIATELY)
        channel = 'la' 
        for k, v in ps.items():
            m = osc_message_builder.OscMessageBuilder(address="/moreheat/video/" + ps['channel'] + "/" + k )
            m.add_arg(v)
            bundle.add_content(m.build())
        bundle = bundle.build()
        self.oscclient.send(bundle)




    def send(self):
        self.oscclient.send_message("/moreheat/test", random.random())

    def beatloop(self):
        print('beat')

    def build_bundle(self):
        bundle = osc_bundle_builder.OscBundleBuilder(osc_bundle_builder.IMMEDIATELY)
        
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
