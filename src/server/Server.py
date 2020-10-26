import os
import argparse
from .ServerCommunicator import ServerCommunicator
from utils import *
from communication import MessageParser
from communication import MessageType
import logging
import threading
import time


class Server:
    __MIN_PERFORMANCE_SCORE_THRESHOLD = 1.5
    __MIN_PERFORMANCE_SCORE = 3.0
    __MAX_UTILIZATION_THRESHOLD = 0.9
    __BATCH_SIZE = 2000000
    __CLIENT_POLL_INTERVAL = 3
    __MAX_GUESS_THRESHOLD = 9999999999
    __MAX_NUMBER_OF_RANGES = 20
    
    
    def __init__(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument('--target', type=str, required=True)
        parser.add_argument('--host', default='127.0.0.1', type=str)
        parser.add_argument('--port', '-p', default=16720, type=int, dest='port')
        args = parser.parse_args(args)

        self.__hash_target = args.target
        self.__ranges_available = []
        self.__hash_result = ''

        self.__cpu_performances = []
        self.__queued_ranges = {}

        self.__server_communicator = ServerCommunicator(args.host, args.port)


    def init(self):
        logging.info(f'Initiating server:')
        logging.debug(self.__server_communicator)
        logging.info(f'Target - {self.__hash_target}')

        threading.Thread(target=self.accept_clients).start()
        
        logging.info('Generating number ranges...')
        self.generate_ranges()
                
    
    def generate_ranges(self):
        for i in range(int(self.__MAX_GUESS_THRESHOLD / self.__BATCH_SIZE) + 1):
            lower = i * self.__BATCH_SIZE
            higher = min(self.__MAX_GUESS_THRESHOLD, (i + 1) * self.__BATCH_SIZE) + 1
            new_range = range(lower, higher)
            self.__ranges_available.append(new_range)


    def accept_clients(self):
        self.__server_communicator.bind()

        while self.__hash_result == '':
            new_id = self.__server_communicator.accept_client()
            thread = threading.Thread(target=self.handle_client, args=(new_id, ))
            thread.setDaemon(True)
            thread.start()


    def handle_client(self, client_id):
        client_name = self.__server_communicator.get_name(client_id)

        if self.__server_communicator.client_exists(client_id):
            self.__server_communicator.send_target(client_id, self.__hash_target)

            while self.__hash_result == '' and self.__server_communicator.client_exists(client_id):
                try:
                    if self.__server_communicator.client_exists(client_id):
                        self.__server_communicator.request_performance(client_id)
                        msg = self.__server_communicator.get_client(client_id).accept_message()
                        client_performance = MessageParser.cpu_performance_from_message(msg)
                    else:
                        break
                    self.__cpu_performances.append(client_performance)
                    
                    capacity = self.get_client_capacity(client_performance)

                    if capacity > 0:
                        self.__queued_ranges[client_id] = []
                        
                        for i in range(capacity):
                            hash_range = self.__ranges_available.pop()
                            
                            if self.__server_communicator.client_exists(client_id):
                                self.__server_communicator.assign_hash_range(client_id, hash_range)
                            else:
                                break

                            logging.info(f'Gave range {hash_range} to {client_name}')

                            self.__queued_ranges[client_id].append(hash_range)


                        while len(self.__queued_ranges[client_id]) > 0 and self.__hash_result == '':
                            # time.sleep(self.__CLIENT_POLL_INTERVAL)
                            
                            if self.__server_communicator.client_exists(client_id): 
                                # self.__server_communicator.send_target(client_id, self.__hash_target)
                                msg = self.__server_communicator.get_client(client_id).accept_message()
                            else:
                                break
                        
                            if msg.get_type() == MessageType.REPORT_RESULT:
                                hash_range = range(int(msg.get_args()['range_start']), int(msg.get_args()['range_end']) + 1)
                                hash_result = str(msg.get_args()['hash_result'])
                                
                                if hash_result != '':
                                    self.__hash_result = hash_result
                                    self.__server_communicator.kill_all()
                                    logging.info(f'Found key - {self.__hash_result}')
                                    break
                                else:
                                    for qrange in self.__queued_ranges[client_id]:
                                        if min(qrange) == min(hash_range) and max(qrange) == max(hash_range):
                                            self.__queued_ranges[client_id].remove(qrange)
                                            logging.info(f'Range {qrange} is now done.')
                            else:
                                raise Exception('Scrambled sequence')
                except:
                    break
        if self.__hash_result == '':
            logging.info(f'{client_name} crashed.')

            if client_id in self.__queued_ranges.keys():
                for qrange in self.__queued_ranges[client_id]:
                    self.__ranges_available.append(qrange)
                    logging.info(f'Adding range back to available ranges - {qrange}')
                
                if client_id in self.__queued_ranges.keys():
                    self.__queued_ranges.pop(client_id)

            if client_id in range(len(self.__cpu_performances)):
                self.__cpu_performances.pop(client_id)

            if self.__server_communicator.client_exists(client_id):
                self.__server_communicator.remove_client(client_id)


    def get_client_capacity(self, cpu_performance):
        if cpu_performance.get_utilization() > self.__MAX_UTILIZATION_THRESHOLD:
            return 0

        if self .__server_communicator.get_number_of_clients() > 1:
            core_counts = []
            frequencies = []
            for performance in self.__cpu_performances:
                core_counts.append(performance.get_cores())
                frequencies.append(performance.get_frequency())

            cores_score = Utils.scale(cpu_performance.get_cores(), min(core_counts), max(core_counts))
            frequency_score = Utils.scale(cpu_performance.get_frequency(), min(frequencies), max(frequencies))
        else:
            cores_score = 1.0
            frequency_score = 1.0

        performance_score = cores_score + frequency_score + cpu_performance.get_utilization()
        
        if performance_score > self.__MIN_PERFORMANCE_SCORE_THRESHOLD:
            return round(Utils.scale(
                performance_score, 
                self.__MIN_PERFORMANCE_SCORE_THRESHOLD, 
                self.__MIN_PERFORMANCE_SCORE, 
                scale=self.__MAX_NUMBER_OF_RANGES))
        else:
            return 0
