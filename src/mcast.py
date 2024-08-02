import sys
import re
import socket
import time
import struct
from netifaces import interfaces, ifaddresses, AF_INET



class Mcast():
    host = 'A'
    addr = '239.192.1.100'
    port = 50000
    testdata = b'hello'
    blocking = True

    def __init__(self, blocking=True):
        self.blocking = blocking
        self.msocket = self.create_socket(self.addr, self.port)
        #time.sleep(1)
        #self.msocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Make the socket multicast-aware, and set TTL.
        #self.msocket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20) # Change TTL (=20) to suit
        # Send the data
        #self.msocket.sendto(self.testdata, (self.addr, self.port))

    def send(self, msg):
        send = False
        while send == False:
            try:
                self.msocket.sendto(msg, (self.addr, self.port))
                send = True
            except BlockingIOError:
                print('blockign')
 

    def recv(self):
        data = b''
        print('rf')
        try:
            data, address = self.msocket.recvfrom(4096)
            print("%s says the time is %s" % (address, data))
        except BlockingIOError:
            print('blocking')
        return data

    def testloop(self):
        while True:
            # Just sending Unix time as a message
            message = str(time.time())

            self.msocket.sendto(message, (self.addr, self.port))
 

    def ip_is_local(self,ip_string):
        """
        Uses a regex to determine if the input ip is on a local network. Returns a boolean.
        It's safe here, but never use a regex for IP verification if from a potentially dangerous source.
        """
        #combined_regex = "(^10\.)|(^172\.1[6-9]\.)|(^172\.2[0-9]\.)|(^172\.3[0-1]\.)|(^192\.168\.)"
        combined_regex = "(^192\.168\.)"
        
        return re.match(combined_regex, ip_string) is not None # is not None is just a sneaky way of converting to a bool

    def get_local_ip(self):
        """
        Returns the first externally facing local IP address that it can find.
        Even though it's longer, this method is preferable to calling socket.gethostbyname(socket.gethostname()) as
        socket.gethostbyname() is deprecated. This also can discover multiple available IPs with minor modification.
        We excludes 127.0.0.1 if possible, because we're looking for real interfaces, not loopback.
        Some linuxes always returns 127.0.1.1, which we don't match as a local IP when checked with ip_is_local().
        We then fall back to the uglier method of connecting to another server.
        """
        local_ips = []
        iplist = [ifaddresses(face)[AF_INET][0]["addr"] for face in interfaces() if AF_INET in ifaddresses(face)]
        for ip in iplist:
            if self.ip_is_local(ip):
                #print( 'local' + ip)
                local_ips.append(ip)

        print(local_ips)
        # socket.getaddrinfo returns a bunch of info, so we just get the IPs it returns with this list comprehension.
        #local_ips = [ x[4][0] for x in socket.getaddrinfo(socket.gethostname(), 80)
        #              if ip_is_local(x[4][0]) ]
        #print(socket.getaddrinfo(socket.gethostname(), 80))
        #print(str(local_ips))
        # select the first IP, if there is one.
        return local_ips[0] if len(local_ips) > 0 else None

    def create_socket(self,multicast_ip, port):
        """
        Creates a socket, sets the necessary options on it, then binds it. The socket is then returned for use.
        """

        local_ip = self.get_local_ip()

        # create a UDP socket
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # allow reuse of addresses
        my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # set multicast interface to local_ip
        my_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(local_ip))

        # Set multicast time-to-live to 2...should keep our multicast packets from escaping the local network
        my_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

        # Construct a membership request...tells router what multicast group we want to subscribe to
        membership_request = socket.inet_aton(multicast_ip) + socket.inet_aton(local_ip)

        # Send add membership request to socket
        # See http://www.tldp.org/HOWTO/Multicast-HOWTO-6.html for explanation of sockopts
        my_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, membership_request)

        if self.blocking == False:
            my_socket.setblocking(0)


        # Bind the socket to an interface.
        # If you bind to a specific interface on the Mac, no multicast data will arrive.
        # If you try to bind to all interfaces on Windows, no multicast data will arrive.
        # Hence the following.
        if sys.platform.startswith("darwin"):
            my_socket.bind(('0.0.0.0', port))
        else:
            my_socket.bind((local_ip, port))

        return my_socket




    def listen_loop(self,multicast_ip, port):
        my_socket = create_socket(multicast_ip, port)

        while True:
            # Data waits on socket buffer until we retrieve it.
            # NOTE: Normally, you would want to compare the incoming data's source address to your own, and filter it out
            #       if it came rom the current machine. Everything you send gets echoed back at you if your socket is
            #       subscribed to the multicast group.
            data, address = my_socket.recvfrom(4096)
            print("%s says the time is %s" % (address, data))

    def announce_loop(self,multicast_ip, port):
        # Offset the port by one so that we can send and receive on the same machine
        my_socket = create_socket(multicast_ip, port + 1)

        # NOTE: Announcing every second, as this loop does, is WAY aggressive. 30 - 60 seconds is usually
        #       plenty frequent for most purposes.
        while True:
            # Just sending Unix time as a message
            message = str(time.time())

            # Send data. Destination must be a tuple containing the ip and port.
            my_socket.sendto(message, (multicast_ip, port))
            time.sleep(1)


