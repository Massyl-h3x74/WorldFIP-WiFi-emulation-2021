#!/usr/bin/env python3
from time import sleep
from argparse import ArgumentParser
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, SO_REUSEPORT
from frame import RP_Dat, ID_Dat

#DEFINING RETURN TIME
_RT = 50


class Producer(object):
    def __init__(self, id: int, data: bytes):
        self._id = id
        self._data = data

    def run_server(self, port=5432):
        self._socket = socket(AF_INET, SOCK_DGRAM)
        self._socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self._socket.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
        self._socket.bind(('', port))
        self.port = port

    def send_rp_dat(self, msg: RP_Dat):
        self._socket.sendto(msg.get_repr(), ('<broadcast>', self.port))

    def recv_id_dat(self):
        data, addr = self._socket.recvfrom(ID_Dat.size())
        try:
            return ID_Dat.from_repr(data)
        except:
            return None

    def do_loop(self):
        while True:
            # 1. Get the ID_Dat
            id_dat = self.recv_id_dat()

            # 2. Ignore messages for which we are not the producer
            if not id_dat or id_dat.id != self._id:
                continue

            # 3. Send back the object to the bus
            sleep(_RT / 1000)
            rp_dat = RP_Dat(self._data)
            print(f'sending {rp_dat}')
            self.send_rp_dat(rp_dat)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('id', type=int)
    parser.add_argument('msg', default='tititata', nargs='?')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    prod = Producer(args.id, bytes(args.msg, 'utf-8'))
    prod.run_server()
    prod.do_loop()
