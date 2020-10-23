import socket
import multiprocessing 

from communication import Communicator
from communication import MessageParser


class ServerCommunicator(Communicator):
    def __init__(self, host: str, port: int):
        super().__init__('ServerCommunicator')
        self.__host = host
        self.__port = port
        
        self.__clients = []


    def bind(self):
        super()._bind(self.__host, self.__port)        


    def accept_message(self, client_id):
        return self.__clients[client_id]._accept_message()
    
    
    def accept_client(self):
        self.__clients.append(super()._accept_client(f'Server{len(self.__clients)} of {self._name}'))
    
    
    def get_number_of_client(self):
        return len(self.__clients)


    def __send_message_to_client(self, client_id, msg):
        client = self.__clients[client_id]
        success = client._send_message(msg)
        if success:
            pass 
        else:
            self.__clients.remove(client)


    def request_performance(self, client_id: int):
        self.__send_message_to_client(client_id, MessageParser.pack_performance_request())


    def assign_hash_key(self, client_id: int, hash_key: str):
        self.__send_message_to_client(client_id, MessageParser.pack_hash_assignment(hash_key))


    def request_hash_results(self, client_id: int):
        self.__send_message_to_client(client_id, MessageParser.pack_hash_results_request())


    def __str__(self):
        string += super().__str__()
        string = f'Port - {self.__port}\n'
        string += f'Host - {self.__host}\n'
        return string