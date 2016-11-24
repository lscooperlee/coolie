
import sys
import os
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.append(os.path.dirname(currentdir))

import struct
import time
import socket
from emilib import emi_init, emi_msg_register, emi_msg, emi_msg_send

from robot.brain.core import cmd2msgnum, ValuedCondition
from robot.brain.cerebellum import uart

addr = "127.0.0.1"

isCmdEnd = ValuedCondition()
def motorCmdEnd(msg):
    isCmdEnd.put(True)

distance = ValuedCondition()
def obstacleDistance(msg):
    distance.put(struct.unpack('ffff', msg.data)[0])

Stucking = False
def motorStuck(msg):
    if not Stucking:
        Stucking = True
        msg = emi_msg(msgnum = ord('m'), cmd = ord('s'), ipaddr = addr, data = struct.pack('=ff', 5, 20))
        emi_msg_send(msg)
        isCmdEnd.get()
        Stucking = False

def obstacleClose(msg):
    while True:
        if not Stucking:
            msg = emi_msg(msgnum = ord('m'), cmd = ord('a'), ipaddr = addr, data = struct.pack('=ff', 5, 3.14))
            emi_msg_send(msg)
            time.sleep(2)
            msg = emi_msg(msgnum = ord('u'), ipaddr = addr)
            emi_msg_send(msg)
            d = distance.get()
            if d > 300:
                break
        else:
            break


def autodrive(addrname = '127.0.0.1'):

    emi_init()

    emi_msg_register(cmd2msgnum(b'ue'), obstacleClose)
    emi_msg_register(cmd2msgnum(b'uu'), obstacleDistance)
    emi_msg_register(cmd2msgnum(b'mk'), motorStuck)
    emi_msg_register(cmd2msgnum(b'me'), motorCmdEnd)

    addr = socket.gethostbyname(addrname)
    print(addr)

    while True:
        msg = emi_msg(msgnum = ord('m'), cmd = ord('w'), ipaddr = addr)
        emi_msg_send(msg)
        time.sleep(100)



if __name__ == '__main__':
    autodrive()
