from multiprocessing import Process
from brain.cerebellum import uart


if __name__ == '__main__':
    uart_read = Process(target = uart.uart_read_run)
    uart_write = Process(target = uart.uart_write_run)

    uart_read.start()
    uart_write.start()

    uart_read.join()
    uart_write.join()
