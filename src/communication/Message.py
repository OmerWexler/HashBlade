from .MessageType import MessageType

class Message:
    def __init__(self, message_type: MessageType, **kwargs):
        self.__type = message_type
        self.__args = kwargs


    def get_type(self) -> MessageType:
        return self.__type


    def get_args(self) -> dict:
        return self.__args


    def __str__(self) -> str:
        return f'Type - {self.__type}({self.__type.value})\n Args - {self.__args}'