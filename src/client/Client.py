import os
import argparse
import time
from .ClientCommunicator import ClientCommunicator

class Client:
    def __init__(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument('-debug', '-d', action='store_true', dest='debug')
        parser.add_argument('--host', default='127.0.0.1', type=str)
        parser.add_argument('--port', '-p', default=16720, type=int, dest='port')
        args = parser.parse_args(args)

        self.__debug = args.debug
        self.__ClientCommunicator = ClientCommunicator(args.host, args.port)

       
    def init(self):
        if self.__debug:
            print(f'Initiating client:')
            print(self.__ClientCommunicator)
