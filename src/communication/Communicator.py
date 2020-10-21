import socket
import communication.Message as m
import communication.MessageParser as mp


class Communicator:
    def __init__(self, name: str, socket_override=None):
        if socket_override == None: 
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self._socket = socket_override
        
        self._name = name


    def accept_message(self):
        length = int(self._socket.read(mp.MessageParser.length_size))
        str_msg = self._socket.read(length)
        
        message = mp.MessageParser.parse_message(str_msg)
        print(f'Recieved - {message}')
        print(f'Raw: - {message.get_raw()}')
        print(f'From: - {self._name}')
        return message


    def send_message(self, message):
        print(f'Sending - {message}')
        print(f'Raw: - {message.get_raw()}')
        print(f'From: - {self._name}')
        self._socket.send(message.get_raw().encode())