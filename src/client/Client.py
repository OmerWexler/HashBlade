import os
import argparse
import time
from .ClientCommunicator import ClientCommunicator

class Client:
    def __init__(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument('--connection-retries', '-r', default=5, type=int, dest='connection_retries')
        parser.add_argument('--connection-interval', '-i', default=3, type=int, dest='connection_interval')
        parser.add_argument('-debug', '-d', action='store_true', dest='debug')
        parser.add_argument('--host', default='127.0.0.1', type=str)
        parser.add_argument('--port', '-p', default=16720, type=int, dest='port')
        args = parser.parse_args(args)

        self.__debug = args.debug
        self.__ClientCommunicator = ClientCommunicator(args.host, args.port, args.connection_interval, args.connection_retries)

       
    def init(self) -> None:
        if self.__debug:
            print(f'Initiating client:')
            print(self.__ClientCommunicator)
