import socket
import multiprocessing 

from communication import Communicator
from communication import MessageParser


class ServerCommunicator(Communicator):
    def __init__(self, host: str, port: int):
        super().__init__('ServerCommunicator')
        self.__host = host
        self.__port = port
        
        self._socket.bind((self.host, self.port))
        self._socket.listen(10)
        
        self.__clients = []


    def accept_client(self):
        while True:
            addr, client = self._socket.accept()
            self.__clients.append(Communicator(f'Client{len(self.__clients)} of {self._name}', client))
            print(f'Client connected from {addr}')
    
    
    def get_number_of_client(self):
        return len(self.__clients)


    def request_performance(self, client_id: int):
        self.__clients[client_id].send_message(MessageParser.pack_performance_request())


    def assign_hash_key(self, client_id: int, hash_key: str):
        self.__clients[client_id].send_message(MessageParser.pack_hash_assignment(hash_key))


    def request_hash_result(self, client_id: int, hash_key: str):
        self.__clients[client_id].send_message(MessageParser.pack_hash_assignment(hash_key))


    def __str__(self):
        string = f'Port - {self.__port}\n'
        string += f'Host - {self.__host}\n'
        return string