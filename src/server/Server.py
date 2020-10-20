import os
import argparse
from .ServerCommunicator import ServerCommunicator


class Server:
    def __init__(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument('--target', type=str, required=True)
        parser.add_argument('--debug', '-d', action='store_true', dest='debug')
        parser.add_argument('--host', default='127.0.0.1', type=str)
        parser.add_argument('--port', '-p', default=16720, type=int, dest='port')
        args = parser.parse_args(args)

        self.__hash_target = args.target
        self.__debug = args.debug

        self.__server_communicator = ServerCommunicator(args.host, args.port)


    def init(self) -> None:
        if self.__debug:
            print(f'Initiating server:')
            print(self.__server_communicator)
            print(f'Target - {self.__hash_target}')