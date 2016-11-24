
import serial
import struct
import emilib
import random

import time

from ..core import common

class ArduinoController:

    class fakeSerial:
        def read(self, b):
            time.sleep(5)
            r = (
                    struct.pack('=bbffff', ord(b'm'), ord(b'c'), 120,121,122,123),
                    struct.pack('=bbffff', ord(b'u'), ord(b'u'), 120,121,122,123),
                )
            return random.choice(r)

        def write(self, b):
            print(b)

    ser = None

    def __init__(self):
        if not self.ser:
            try:
                self.ser = serial.Serial('/dev/ttyUSB0', 9600)
            except:
                self.ser = self.fakeSerial()


    def send_cmd(self, cmd, subcmd=0, param0 = 0, param1 = 0, param2 = 0, param3 = 0):

        if type(cmd) is bytes:
            cmd = ord(cmd)

        if type(subcmd) is bytes:
            subcmd = ord(subcmd)

        sendcmd = struct.pack('=bbffff', cmd, subcmd, param0, param1, param2, param3)
        self.ser.write(sendcmd)

    def read_cmd(self):
        return self.ser.read(18)

controller = ArduinoController()

def motorControl(msg):
    param0, param1 = struct.unpack('=ff', msg.data) if msg.data else (0, 0)
    controller.send_cmd(msg.msg, msg.cmd, param0, param1)

def uart_read_run():
    while True:
        ret = controller.read_cmd()
        msg = emilib.emi_msg(msgnum = common.cmd2msgnum(ret[:2]) ,
                             cmd = ret[1], data=ret[2:])
        emilib.emi_msg_send(msg)


def uart_write_run():
    emilib.emi_init()
    emilib.emi_msg_register(common.cmd2msgnum('m'), motorControl)
    emilib.emi_msg_register(common.cmd2msgnum('u'), motorControl)
    emilib.emi_loop()
