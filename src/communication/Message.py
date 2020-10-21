import communication.MessageType as mt

class Message:
    def __init__(self, message_type: mt.MessageType, raw_message: str, args: dict):
        self.__type = message_type
        self.__args = args
        self.__raw_message = raw_message


    def get_type(self):
        return self.__type


    def get_args(self):
        return self.__args


    def get_raw(self):
        return self.__raw_message


    def __str__(self):
        return f'Type - {self.__type}({self.__type.value})\nArgs - {self.__args}'