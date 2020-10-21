# from .MessageType import MessageType 
import communication.MessageType as mt

class Message:
    def __init__(self, message_type: mt.MessageType, **kwargs):
        self.__type = message_type
        self.__args = kwargs


    def get_type(self):
        return self.__type


    def get_args(self):
        return self.__args


    def __str__(self):
        return f'Type - {self.__type}({self.__type.value})\n Args - {self.__args}'