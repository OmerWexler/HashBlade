class Message:
    def __init__(self, message_type, raw_message: str, args: dict):
        self.__type = message_type
        self.__args = args

        if isinstance(raw_message, bytes):
            self.__raw_message = raw_message.decode()
        else:
            self.__raw_message = raw_message


    def get_type(self):
        return self.__type


    def get_args(self):
        return self.__args


    def get_raw(self):
        return self.__raw_message


    def __str__(self):
        return f'Message:\nType - {self.__type}({self.__type.value})\nArgs - {self.__args}'