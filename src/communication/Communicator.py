import socket
import communication.Message as m
import communication.MessageParser as mp


class Communicator:
    def __init__(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def accept_message(self):
        length = int(self.__socket.read(mp.MessageParser.length_size))
        msg = self.__socket.read(length)

        return mp.MessageParser.parse_message(msg)
