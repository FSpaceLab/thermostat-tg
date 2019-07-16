import socket
import re
from .settings import *



class ThermostatBox:
    def __init__(self):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = (SOCK_HOST, SOCK_PORT)

        self.sock.connect(server_address)

    def send_data_to_box(self, text):
        try:
            self.sock.sendall(text.encode())

        finally:
            self.sock.close()

    def get_data_from_box(self):
        res = ''
        try:

            # Send data
            message = GET_DATA.encode()

            self.sock.sendall(message)

            # Look for the response
            amount_received = 0
            amount_expected = len(message)

            while amount_received < amount_expected:
                data = self.sock.recv(1024)
                amount_received += len(data)
                res = re.findall(pattern, data.decode())
        finally:

            self.sock.close()
            return res
