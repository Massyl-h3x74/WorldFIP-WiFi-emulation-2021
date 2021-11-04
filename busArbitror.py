#!/usr/bin/env python3
from time import sleep
from math import gcd
from functools import reduce
from itertools import cycle
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, SO_REUSEPORT
from frame import ID_Dat

#DEFINE RETURN TIME
_RT = 50
class BusArbitror(object):
    '''
    Représente un arbitre de bus du protocol World-FIP
    '''
    def __init__(self, table={}):
        self._table = table
        self._microcycle, self._macrocycle = self.cycles_from_table(table)

    def run_server(self, port=5432):
        self._socket = socket(AF_INET, SOCK_DGRAM)
        self._socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self._socket.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
        self._socket.settimeout(0)
        self._socket.bind(('', port))
        self.port = port

    def send_msg(self, msg: bytes):
        self._socket.sendto(msg, ('<broadcast>', self.port))

    def do_loop(self):
        '''
        Loop over all messages and schedule IDs according to the table
        '''
        tmp2 = None
        for tmp, msg in cycle(self.list_macrocycle()):
            if tmp != tmp2:
                tmp2 = tmp
                sleep(self._microcycle  / 1000)
                print(f"tmp = {tmp} ms")
            # Sent the message over the bus
            print(f'\tSending  message : [{msg}]')
            self.send_msg(msg.get_repr())
            sleep((3 * _RT)  / 1000)

    def list_macrocycle(self):
        '''
        Do a full macrocycle

        return a tuple `(time, Frame)`
        '''
        for tmp in range(0, self._macrocycle, self._microcycle):
            # Loop over the table to see what message should be send
            for id, period in self._table.items():
                if tmp % period == 0:
                    yield (tmp, ID_Dat(id))

    @staticmethod
    def cycles_from_table(table):
        '''Return the microcycle and macrocycle from a period table'''
        def ppcm(values):
            '''Helper to compute the Least Commom Multiple'''
            return reduce(lambda x, y: x * y // gcd(x, y), values)
        return (min(table.values()), ppcm(table.values()))


if __name__ == '__main__':
    table = {
        101: 100 * 10,
        102: 200 * 10,
        103: 500 * 10,
        104: 100 * 10,
        105: 200 * 10,
    }

    bus = BusArbitror(table)
    bus.run_server()
    bus.do_loop()
