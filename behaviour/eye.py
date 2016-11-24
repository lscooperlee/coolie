from multiprocessing import Process
from emilib import emi_init, emi_msg_register, emi_msg, emi_msg_send

from brain.core import cmd2msgnum, ValuedCondition
from brain.sense.eye import open_eye

if __name__ == '__main__':
    #eye = Process(target = open_eye, args=((128, 128),))
    eye = Process(target = open_eye, args=((320, 240),))
    eye.start()
    eye.join()
