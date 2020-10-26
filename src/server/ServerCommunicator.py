import socket
import multiprocessing 

from communication import Communicator
from client.ClientCommunicator import ClientCommunicator
from communication import MessageParser


class ServerCommunicator(Communicator):
    def __init__(self, host: str, port: int):
        super().__init__('ServerCommunicator')
        self.__host = host
        self.__port = port
        
        self.__clients = []


    def bind(self):
        super()._bind(self.__host, self.__port)        


    def get_name(self, client_id):
        return self.__clients[client_id].get_name()


    def accept_message(self, client_id):
        try:
            return self.__clients[client_id].accept_message()
        except:
            self.__clients.pop(client_id)

    
    def accept_client(self):
        self.__clients.append(Communicator(f'Server{len(self.__clients)} of {self._name}', socket_override=super()._accept_client()))
        return len(self.__clients) - 1
    
    
    def client_exists(self, client_id):
        return self.get_number_of_clients() > client_id; 


    def get_number_of_clients(self):
        return len(self.__clients)


    def __send_message_to_client(self, client_id, msg):
        client = self.__clients[client_id]
        success = client.send_message(msg)
        if success:
            pass 
        else:
            self.__clients.remove(client)


    def request_performance(self, client_id: int):
        self.__send_message_to_client(client_id, MessageParser.pack_performance_request())


    def assign_hash_range(self, client_id: int, hash_range: list):
        self.__send_message_to_client(client_id, MessageParser.pack_hash_assignment(hash_range))


    def request_hash_results(self, client_id: int, hash_target: str):
        self.__send_message_to_client(client_id, MessageParser.pack_hash_results_request(hash_target))


    def kill_all(self):
        for client in self.__clients: 
            client.send_message(MessageParser.pack_kill_request())
            client._disconnect()

        self.__clients = []

    
    def __str__(self):
        string += super().__str__()
        string = f'Port - {self.__port}\n'
        string += f'Host - {self.__host}\n'
        return string