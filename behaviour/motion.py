from multiprocessing import Process
from emilib import emi_init, emi_msg_register, emi_msg, emi_msg_send

from brain.core import cmd2msgnum, ValuedCondition
from brain.cerebellum import uart


if __name__ == '__main__':
    uart_read = Process(target = uart.uart_read_run)
    uart_write = Process(target = uart.uart_write_run)

    uart_read.start()
    uart_write.start()

    uart_read.join()
    uart_write.join()
