import struct
import time
import socket
import os
import itertools
import numpy as np
from PIL import Image
from multiprocessing import Process
from emilib import emi_init, emi_msg_register, emi_msg, emi_loop

from brain.core import cmd2msgnum, ValuedCondition
from brain.cerebellum import uart
from brain.cortex.cbrain import network

motorCmdValue = ValuedCondition()
imageValue = ValuedCondition()

def motorCommand(msg):
    motorCmdValue.put([1 if msg.cmd==ord(x) else 0 for x in 'asdw'])

def imageData(msg):
    imageValue.put(msg.data)

def data_collect():
    DATA_PATH='/tmp/drive_data/'
    if os.path.exists(DATA_PATH):
        os.rename(DATA_PATH, '/tmp/drive_data_backup')

    os.mkdir(DATA_PATH)

    emi_init()
    emi_msg_register(cmd2msgnum('m'), motorCommand)
    emi_msg_register(1, imageData)

    suffix = 0
    while True:
        suffix += 1
        key = motorCmdValue.get()
        img = imageValue.peek()
        if img:
            mname = '{2}/{1:0>5d}_{0[0]}{0[1]}{0[2]}{0[3]}' \
                    '.jpg'.format(key, suffix, DATA_PATH)
            with open(mname, 'wb') as fd:
                fd.write(img)

def train():
    net = network.FFN((128*128, 1024, 4))

    def training_data_iter():
        DATA_PATH='/tmp/drive_data/'
        for name in os.listdir(DATA_PATH):
            pil_im = Image.open(DATA_PATH+name).convert('L')
            data = np.array(pil_im)
            label = np.array([int(x) for x in name[6:10]])
            yield data.reshape(-1), label

    train_iter = itertools.islice(net.train(training_data_iter()), 5)

    for n, s in enumerate(train_iter):
        print(n, s)


def test_forward(self):
    net = FFN((1, 2, 1))
    net.T["W01"] = np.array([[3, 1]])
    net.T["W12"] = np.array([[2], [1]])
    net.T["B1"] = np.array([1, 1])
    net.T["B2"] = np.array([1])
    net.F = Line()

    dg = IntegerDataGenerator()
    idata = dg.get(1, 3, 1)
    odata = np.array([net.forward(v) for v in idata])

    assert_array_equal(odata, np.array([[11], [18]]))

if __name__ == '__main__':
    data_collect()
    #train()
