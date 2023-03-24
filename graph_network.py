import socket
from multiprocessing import Process
import multiprocessing as mp
import argparse
import time

class server():

    def __init__(self, ip_addr: str, port: int):
        self.ip_addr = ip_addr
        self.port = port

        self.init_socket()
        self.start_listening()
        self.init_game()
        self.cleanup()

    def init_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_listening(self):
        self.socket.bind((self.ip_addr, self.port))
        self.socket.listen()

    def init_game(self):
        partner_socket, partner_addr = self.socket.accept()
        print('Game started.')
        msg = partner_socket.recv(1024).decode()
        print(f'Received message {msg}')
    
    def cleanup(self):
        self.socket.close()


class client():

    def __init__(self, server_addr: str, server_port: int):
        self.server_addr = server_addr
        self.server_port = server_port

        self.init_socket()
        self.connect_to_server()
        self.start_game()
        self.cleanup()

    def init_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self):
        self.socket.connect((self.server_addr, self.server_port))
        # while True:
        #     try:
        #         self.socket.connect((self.server_addr, self.server_port))
        #     except Exception as e:
        #         print(e)
        #         time.sleep(1)

    def start_game(self):
        msg = 'Hello, server!'
        self.socket.send(msg.encode())
    
    def cleanup(self):
        self.socket.close()

def _create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--client-ip', type=str)
    parser.add_argument('--server-ip', type=str)
    parser.add_argument('--client-port', type=int)
    parser.add_argument('--server-port', type=int)
    return parser

if __name__=='__main__':
    mp.set_start_method('fork')

    parser = _create_parser()
    args = parser.parse_args()

    server = Process(target=server, args=(args.server_ip, args.server_port))
    server.start()
    
    inp = input('Start connection? [y/n]: ')
    if inp.lower() == 'y':
        client = Process(target=client, args=(args.client_ip, args.client_port))
        client.start()
    
        server.join()
        client.join()
    else:
        server.join()