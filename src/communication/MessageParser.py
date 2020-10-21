# from .MessageType import MessageType
# from .Message import Message
import communication.Message as m
import communication.MessageType as mt

class MessageParser:
    __seperator = '@@@'
    
    @staticmethod
    def generate_format(message_type: int, args: list):
        sep = MessageParser.__seperator
        message_type = str(message_type)
        wrapped_args = []

        for arg in args:
            arg = '{' + arg + '}'
            wrapped_args.append(arg)

        return str(message_type.zfill(2) + sep + sep.join(wrapped_args))


    # type@@@arg@@@arg@@@arg...
    @staticmethod
    def parse_message(message: str):
        message = message.split(MessageParser.__seperator)
        
        message_type = message.pop(0)
        message_type = mt.MessageType[message_type]