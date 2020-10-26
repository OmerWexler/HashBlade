import time
import socket

from communication import Communicator
from communication import MessageParser
from utils import CPUPerformance


class ClientCommunicator(Communicator):
    def __init__(self, host: str, port: int):
        super().__init__('ClientCommunicator')
        self.__host = host
        self.__port = port


    def connect(self):
        super()._connect(self.__host, self.__port)


    def accept_message(self):
        return super().accept_message()


    def report_performance(self, CPUPerformance):
        self.send_message(MessageParser.pack_performance_report(CPUPerformance))


    def report_hash_result(self, hash_range, hash_result):
        self.send_message(MessageParser.pack_hash_result_report(hash_range, hash_result))


    def disconnect(self):
        super()._disconnect()

    
    def __str__(self):
        string = ''
        string += super().__str__()
        string = f'Port - {self.__port}\n'
        string += f'Host - {self.__host}\n'
        return string