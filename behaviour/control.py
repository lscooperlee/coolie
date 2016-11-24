import struct
import socket
import sys
import tty
import termios
from functools import partial
from emilib import emi_init, emi_msg_register, emi_msg, emi_msg_send

from brain.core import cmd2msgnum, ValuedCondition
from brain.cerebellum import uart

addr = "127.0.0.1"

motorCounter = ValuedCondition()
def motorCounterHandler(msg):
    motorCounter.put(struct.unpack('ffff', msg.data)[:2])
    print(motorCounter.peek())

distance = ValuedCondition()
def obstacleDistance(msg):
    distance.put(struct.unpack('ffff', msg.data)[0])
    print(distance.peek())

def getchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def calibrate():

    msg = emi_msg(msgnum = ord('u'), ipaddr = addr)
    emi_msg_send(msg)
    d1 = distance.get()

    msg = emi_msg(msgnum = ord('m'), cmd = ord('c'), ipaddr = addr)
    emi_msg_send(msg)
    c1 = motorCounter.get()

    msg = emi_msg(msgnum = ord('m'), cmd = ord('w'), ipaddr = addr)
    emi_msg_send(msg)
    d2 = distance.get()

    msg = emi_msg(msgnum = ord('m'), cmd = ord('c'), ipaddr = addr)
    emi_msg_send(msg)
    c2 = motorCounter.get()
    print(c1,c2,d1,d2)

    c = (c2[0] + c2[1])/2 - (c1[0] + c1[1])/2
    d = d1 - d2
    if d == 0:
        return None
    else:
        return c/d




def run(addrname = 'pi3wifi'):
    emi_init()

    emi_msg_register(cmd2msgnum(b'uu'), obstacleDistance)
    emi_msg_register(cmd2msgnum(b'mc'), motorCounterHandler)

    addr = socket.gethostbyname(addrname)

    msgdict = {
            'w': emi_msg(msgnum = ord('m'), cmd = ord('w'),
                data=struct.pack('=ff', 1, 0)), #forward, default speed 1
            's': emi_msg(msgnum = ord('m'), cmd = ord('s'),
                data=struct.pack('=ff', 1, 0)), #backward default speed 1
            'a': emi_msg(msgnum = ord('m'), cmd = ord('a'),
                data=struct.pack('=ff', 5, 0)), #left turn, default speed 5
            'd': emi_msg(msgnum = ord('m'), cmd = ord('d'),
                data=struct.pack('=ff', 5, 0)), #right turn, default speed 5
            'n': emi_msg(msgnum = ord('m'), cmd = ord('n'), ipaddr = addr),
            'c': emi_msg(msgnum = ord('m'), cmd = ord('c'), ipaddr = addr),
            'u': emi_msg(msgnum = ord('u'), ipaddr = addr),
            'r': calibrate,
            }

    while True:
        c = getchar()
        if c is 'q':
            break

        if c in msgdict:
            ret = emi_msg_send(msgdict[c])
            print("send ", c, ret)
        elif c in '12345':
            msgdata = struct.pack('=ff', float(c), 0)
            msg = emi_msg(msgnum=ord('m'), cmd=ord('u'), data=msgdata)
            ret = emi_msg_send(msg)
            print("send ", 'm', ret)


if __name__ == '__main__':

    run("127.0.0.1") #block
