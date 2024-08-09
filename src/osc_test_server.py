"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""
import argparse
import math

from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server

from typing import List, Any
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient

def msgprint(address: str, *args: List[Any]) -> None:
  try:
    #print("[{0}] ~ {1}".format(args[0], args[1](volume)))

    print(address, str(args[0]))
  except (ValueError, IndexError):
      print('va: ' + address + ' lenargs:  ' + str(len(args)))



if __name__ == "__main__":
    dispatcher = Dispatcher()
    #dispatcher.map("/filter", print)
    #dispatcher.map("/volume", print_volume_handler, "Volume")
    #dispatcher.map("/logvolume", print_compute_handler, "Log volume", math.log)
    dispatcher.map("/moreheat/*", msgprint)  # Map wildcard address to set_filter function


    server = osc_server.ThreadingOSCUDPServer(
      ("127.0.0.1", 5005), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
