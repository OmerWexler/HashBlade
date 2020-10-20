import time
import socket

class ClientCommunicator:
    def __init__(self, host: str, port: int, connection_interval: int, connection_retries: int):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__host = host
        self.__port = port

        self.__connection_interval = connection_interval
        self.__connection_retries = connection_retries


    def connect(self) -> bool:
        for i in range(self.__connection_retries):
            try:
                if dubug: print(f'Attempting connection to - ({self.__host}, {self.__port})...')
                self.__socket.connect((self.__host, self.__port))
                if dubug: print(f'Connection to server at - ({self.__host}, {self.__port}) successful.')
                return True
            except ConnectionRefusedError:
                self.print(f'Failed to connect to - ({self.__host}, {self.__port}), {self.__connection_retries - i} retries left...\n')
                for i in range(self.__connection_interval):
                    if debug: print(f'Retrying to connect in {self.__connection_interval - i}')
                    time.sleep(1)
    
        self.print(f'Failed to connect to - ({self.host}, {self.__port}).')
        self.print('No more retries left, exiting...')
        return False


    def __str__(self) -> str:
        string = f'Port - {self.__port}\n'
        string += f'Host - {self.__host}\n'
        string += f'Connection retries - {self.__connection_retries}\n'
        string += f'Connection interval - {self.__connection_interval}'
        return string