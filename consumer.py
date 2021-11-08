#!/usr/bin/env python3
from time import sleep
from argparse import ArgumentParser
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, SO_REUSEPORT
from frame import RP_Dat, ID_Dat

import RPi.GPIO as GPIO #Importe la bibliothèque pour contrôler les GPIOs

GPIO.setmode(GPIO.BOARD) #Définit le mode de numérotation (Board)
GPIO.setwarnings(False) #On désactive les messages d'alerte

RED_LED = 7 #Définit le numéro du port GPIO qui alimente la led
GREEN_LED = 11
GPIO.setup(RED_LED, GPIO.OUT) #Active le contrôle du GPIO
GPIO.setup(GREEN_LED, GPIO.OUT) #Active le contrôle du GPIO

#DEFINING RETURN TIME
_RETURN_TIME = 50

class Consumer(object):
    def __init__(self, id: int):
        self._id = id
        self._data = None
        self._cons_time = (_RETURN_TIME/4)-3
    def server_init(self, port=5432):
        self._socket = socket(AF_INET, SOCK_DGRAM)
        self._socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self._socket.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
        self._socket.bind(('', port))
        self._port = port

    def recv_id_dat(self, data=None):
        if not data:
            data, addr = self._socket.recvfrom(ID_Dat.size())
        try:
            return ID_Dat.from_repr(data)
        except:
            return "Data not recieved"

    def recv_rp_dat(self):
        old_to = self._socket.gettimeout()
        self._socket.settimeout(2 * _RETURN_TIME / 1000)
        try:
            data, addr = self._socket.recvfrom(RP_Dat.size())
        finally:
            self._socket.settimeout(old_to)

        try:
            return (True, RP_Dat.from_repr(data))
        except:
            return (False, data)

    def loop_init(self):
        data = None
        recv_val = RP_Dat.from_repr(data)
        val = len(RP_Dat.from_repr(data))/2
        while True:
            GPIO.output(RED_LED, GPIO.LOW)
            GPIO.output(GREEN_LED,GPIO.HIGH)
            # 1. Get the ID_Dat, use the existing one if exists
            id_dat = self.recv_id_dat()

            # 2. Ignore messages for which we are not a consumer
            if not id_dat or id_dat.id != self._id:
                continue

            state = GPIO.input(RED_LED) #Lit l'état actuel du GPIO, vrai si allumé, faux si éteint
            if state : #Si GPIO allumé
                GPIO.output(RED_LED, GPIO.LOW) #On l’étein
                GPIO.output(GREEN_LED,GPIO.HIGH)
            else:
                GPIO.output(GREEN_LED,GPIO.LOW)
                GPIO.output(RED_LED,GPIO.HIGH)

            # 4. Get the object from the bus
            sleep( _RETURN_TIME  / 1000)
            try:
                ok, rp_dat = self.recv_rp_dat()
            except:
                print('Timeout reached, ignoring...')
                continue
            if not ok:
                data = rp_dat
                continue

            # 4.5 It worked
            print(f'Received: DATA=[{rp_dat}]')
            if len(recv_val) >= (val+(val*0.2)):
                GPIO.output(RED_LED, GPIO.HIGH) #On l'allume
                sleep(self._cons_time*0.2)
            GPIO.output(GREEN_LED,GPIO.LOW)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('id', type=int)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    prod = Consumer(args.id)
    prod.server_init()
    prod.loop_init()
