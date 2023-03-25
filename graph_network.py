import socket
from multiprocessing import Process
import argparse
import time

class Server(Process):

    def __init__(self, ip_addr: str, port: int):
        super().__init__()
        self.ip_addr = ip_addr
        self.port = port
        self.turn = 0

    def run(self):
        self.init_socket()
        self.start_listening()
        self.init_game()
        self.cleanup()

    def init_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_listening(self):
        self.socket.bind((self.ip_addr, self.port))
        self.socket.listen()

        self.socket1, addr1 = self.socket.accept()
        msg = 'Connection made.'
        self.socket1.send(msg.encode())

        self.socket2, addr2 = self.socket.accept()
        self.socket2.send(msg.encode())

    def init_game(self):
        while True:
            if self.turn % 2 == 0:
                action = self.socket1.recv(1024).decode()
                # ...
                msg = f'Turn {self.turn}'
                self.socket2.send(msg.encode())
            else:
                action = self.socket2.recv(1024).decode()
                # ...
                msg = f'Turn {self.turn}'
                self.socket1.send(msg.encode())
            self.turn += 1
    
    def cleanup(self):
        self.socket.close()


class Client(Process):

    def __init__(self, server_addr: str, server_port: int, is_first: bool):
        super().__init__()
        self.server_addr = server_addr
        self.server_port = server_port
        self.is_first = is_first

    def run(self):
        self.init_socket()
        self.connect_to_server()
        self.start_game()
        self.cleanup()

    def init_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self):
        self.socket.connect((self.server_addr, self.server_port))
        msg = self.socket.recv(1024).decode()
        print(msg)

    def start_game(self):
        time.sleep(4)
        while True:
            if self.is_first:
                msg = 'Action'
                self.socket.send(msg.encode())
            else:
                msg = self.socket.recv(1024).decode()
                print(msg)
            self.is_first = not self.is_first
    
    def cleanup(self):
        self.socket.close()

def _create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--server-ip', type=str)
    parser.add_argument('--server-port', type=int)
    parser.add_argument('--first-player', action='store_true')
    return parser

if __name__=='__main__':
    parser = _create_parser()
    args = parser.parse_args()

    if args.first_player:
        server = Server(args.server_ip, args.server_port)
        server.start()
        time.sleep(1)
    
    client = Client(args.server_ip, args.server_port, args.first_player)
    client.start()