import struct
import time
import socket
import os
import itertools
import pickle
import io
from PIL import Image
from multiprocessing import Process
import numpy as np
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

            print("data %s saved"%mname)


def prepare_data(img):
    fd = io.BytesIO(img)
    pil_im = Image.open(fd).convert('L').resize((32, 24))
    return np.array(pil_im).reshape(-1)


def train(data_path='/tmp/drive_data/', net_file='auto.net', iterloop=1000):
    net = network.FFN((32*24, 1024, 4))

    def training_data_iter():
        for name in os.listdir(data_path):
            with open(data_path + name, 'rb') as fd:
                data = prepare_data(fd.read())
                label = np.array([int(x) for x in name[6:10]])

                yield data.reshape(-1), label

    train_iter = itertools.islice(net.train(training_data_iter()), iterloop)

    for n, s in enumerate(train_iter):
        print(n, s)

    return net


def drive(img, net):
    data = prepare_data(img)
    return np.argmax(net.forward(data))


if __name__ == '__main__':
    #data_collect()

    net = train(iterloop=6)

    pickle.dump(net, open('auto.net', 'wb'))
    pickle.load(open('auto.net', 'rb'))

    with open('/tmp/drive_data/00001_1000.jpg', 'rb') as fd:
        img = fd.read()
        d = drive(img, net)
        print(d)
