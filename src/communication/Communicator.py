import socket
import time
import communication.MessageParser as mp


class Communicator:
    def __init__(self, name: str, socket_override=None):
        if isinstance(socket_override, socket.socket): 
            self._socket = socket_override
        else:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self._name = name
        self._connected = False


    def _accept_message(self):
        length = int(self._socket.recv(mp.length_size))
        str_msg = self._socket.recv(length).decode()
        
        message = mp.parse_message(str_msg)
        print(f'{self._name} recieved - {message}')
        print(f'Raw: - {message.get_raw()}')
        return message


    def _send_message(self, message):
        try:
            print(f'{self._name} sending - {message}')
            print(f'Raw: - {message.get_raw()}')
            self._socket.send(message.get_raw().encode())
            return True
        except ConnectionError:
            print(f'{self._name} couldn\'t send:\n{message}\nTo {self._socket.getpeername()}.')
            self._disconnect()
            return False
    

    def _accept_client(self, client_name):
        print(f'{self._name} waiting for client...')
        client, addr = self._socket.accept()
        print(f'Client connected to {self._name} from {addr}')
        return Communicator(client_name, socket_override=client)


    def _connect(self, host: str, port: int):
        try:
            print(f'{self._name} attempting connection to - {host}:{port}...')
            self._socket.connect((host, port))
            print(f'{self._name} connected to - {host}:{port} successful.')
            return True
        except ConnectionRefusedError:
            while not self._connected:
                print(f'Failed to connect to - {host}:{port}.')
                for i in range(3):
                    print(f'Retrying to connect in {3 - i}')
                    time.sleep(1)
                
                try:
                    self._socket.connect((host, port))
                    self._connected = True
                except ConnectionRefusedError:
                    pass
                
        print(f'{self._name} connected to {host}:{port}')

    
    def _bind(self, host: str, port: int):
        self._socket.bind((host, port))
        self._socket.listen(10)
        print(f'{self._name} binded to {host}:{port}')


    def _disconnect(self):
        peer_name = self._socket.getpeername()
        self._socket.close()
        print(f'{self._name} diconnected from {peer_name}...')