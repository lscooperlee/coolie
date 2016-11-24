import struct
import time
import socket
from multiprocessing import Process
from emilib import emi_init, emi_msg_register, emi_msg, emi_msg_send

from brain.core import cmd2msgnum, ValuedCondition
from brain.cerebellum import uart

addr = "127.0.0.1"

motorCounter = ValuedCondition()
def motorCounterHandler(msg):
    motorCounter.put(struct.unpack('ffff', msg.data)[:2])

distance = ValuedCondition()
def obstacleDistance(msg):
    distance.put(struct.unpack('ffff', msg.data)[0])


def autodrive(addrname = '127.0.0.1'):

    emi_init()

    emi_msg_register(cmd2msgnum(b'uu'), obstacleDistance)
    emi_msg_register(cmd2msgnum(b'mc'), motorCounterHandler)

    addr = socket.gethostbyname(addrname)
    print(addr)

    while True:

        while True:

            msg = emi_msg(msgnum = ord('m'), cmd = ord('c'), ipaddr = addr)
            ret = emi_msg_send(msg)
            c = motorCounter.get()
            print(c)

            msg = emi_msg(msgnum = ord('u'), ipaddr = addr)
            ret = emi_msg_send(msg)

            d = distance.get()
            print(d)
            if d < 300:

                msg = emi_msg(msgnum = ord('m'), cmd = ord('a'), ipaddr = addr, data = struct.pack('=ff', 5, 3.14/2))
                ret = emi_msg_send(msg)

            else:
                break

            time.sleep(1)
            msg = emi_msg(msgnum = ord('m'), cmd = ord('c'), ipaddr = addr)
            ret = emi_msg_send(msg)
            c1 = motorCounter.get()
            print(c1)

            if c1[0] - c[0] < 10:
                msg = emi_msg(msgnum = ord('m'), cmd = ord('a'), ipaddr = addr, data = struct.pack('=ff', 5, 3.14/2))
                ret = emi_msg_send(msg)

            time.sleep(1)


        msg = emi_msg(msgnum = ord('m'), cmd = ord('w'), ipaddr = addr)
        ret = emi_msg_send(msg)

        d = distance.get()
        print(d)

if __name__ == '__main__':
    autodrive()
