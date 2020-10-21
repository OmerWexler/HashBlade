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
    def parse_message(raw_message: str):
        message_type = raw_message.split(MessageParser.__seperator)[0]
        message_type = mt.MessageType.translate_from_id(message_type)
        
        message_args_names = message_type.value.replace('{', '').replace('}', '').split(MessageParser.__seperator)[1:]
        message_args_values = raw_message.split(MessageParser.__seperator)[1:]

        if len(message_args_names) != len(message_args_values):
            raise InvalidNumberOfArguments(len(message_args_names), len(message_args_values))

        message_args = {}
        for i in range(len(message_args_names)):
            message_args[message_args_names[i]] = message_args_values[i]

        return m.Message(message_type, raw_message, message_args)

    


class ParseError(Exception):
    def __init__(self, parse_error, raw_message):
        super().__init__(f'Parsing of {parse_error} failed - {raw_message}')


class InvalidNumberOfArguments(ParseError):
    def __init__(self, number_of_raw_arguments, number_of_actual_arguments):
        super.__init__(f'number of required arguments - {number_of_raw_arguments} but received - {number_of_actual_arguments} arguments.')
