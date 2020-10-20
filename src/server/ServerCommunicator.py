import socket
import multiprocessing 

class ServerCommunicator:
    def __init__(self, host: str, port: int):
        self.__host = host
        self.__port = port
        
        self.__hs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__hs.bind((self.host, self.port))
        self.__hs.listen(10)
        self.__clients = []
        self.__client_threads = []

        self.__client_accept_thread = None
        

    def start_accepting_clients(self) -> None:
        self.__client_accept_thread = multiprocessing.Process(target=self.__accept_clients)
        self.__client_accept_thread.daemon = True
        self.__client_accept_thread.start()


    def accept_clients(self) -> None:
        print('Starting to accept clients.')
        while True:
            addr, client = self.__hs.accept()
            self.__clients.append(client)
            self.__client_threads.append(multiprocessing.Process(target=self.__accept_clients), args=(client))
            print(f'Client connected from {addr}')
    
    
    def __str__(self) -> str:
        string = f'Port - {self.__port}\n'
        string += f'Host - {self.__host}\n'
        return string