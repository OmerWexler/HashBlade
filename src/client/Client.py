import os
import argparse
import time
from .ClientCommunicator import ClientCommunicator
import logging
from communication import MessageType
from communication import MessageParser
from utils import PerformanceCalculator
import hashlib
import threading


class Client:
    def __init__(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument('--host', default='127.0.0.1', type=str)
        parser.add_argument('--port', '-p', default=16720, type=int, dest='port')
        args = parser.parse_args(args)

        self.__client_communicator = ClientCommunicator(args.host, args.port)
        self.__performance_calculator = PerformanceCalculator()
        self.__results = {}
        self.__completed_ranges = []
        self.__threads_sum = 0
        self.__target = ''


    def init(self):
        logging.debug(f'Initiating client:')
        logging.debug(self.__client_communicator)
        self.__client_communicator.connect()
        msg_type = None

        while msg_type != MessageType.KILL:
            msg = self.__client_communicator.accept_message()
            msg_type = msg.get_type()
            
            if msg.get_type() == MessageType.SET_TARGET:
                hash_target = msg.get_args()['hash_target']
                self.__target = hash_target

            if msg.get_type() == MessageType.ASSIGN_HASH:
                if self.__threads_sum == 0: # All ranges done, so clear
                    self.__results = {}
                hash_range = range(int(msg.get_args()['range_start']), int(msg.get_args()['range_end']) + 1)
                thread = threading.Thread(target=self.proccess_hash_range, args=(hash_range, ))
                thread.setDaemon(True)
                thread.start()
                self.__threads_sum += 1
            
            elif msg.get_type() == MessageType.REQUEST_PERFORMANCE:
                self.__client_communicator.report_performance(self.__performance_calculator.analyze_cpu_performance())

        self.__client_communicator.disconnect()


    def proccess_hash_range(self, hash_range):
        logging.info(f'Starting range {hash_range}')
        for i in hash_range:
            hash_candidate = str(i).zfill(10)
            hash_result = hashlib.md5(hash_candidate.encode()).hexdigest().upper()

            if self.__target == hash_result:
                self.__client_communicator.report_hash_result(hash_range, hash_candidate)


        self.__client_communicator.report_hash_result(hash_range, '')
        self.__completed_ranges.append(hash_range)
        self.__threads_sum -= 1
        logging.info(f'Finished range {hash_range}')
