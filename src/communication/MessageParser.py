import communication.Message as Message
import communication.MessageType as mt
from utils import CPUPerformance


class MessageParser:
    seperator = '@@@'
    length_size = 2 # bytes


    # type@@@arg@@@arg@@@arg...
    @staticmethod
    def parse_message(raw_message: str):
        message_type = raw_message.split(MessageParser.seperator)[0]
        message_type = mt.MessageType.translate_from_id(message_type)
        
        # message_args_names = message_type.value.replace('{', '').replace('}', '').split(MessageParser.seperator)[1:]
        message_args_names = message_type.value.get_args_names()
        message_args_values = raw_message.split(MessageParser.seperator)[1:]

        if len(message_args_names) != len(message_args_values):
            raise InvalidNumberOfArguments(len(message_args_names), len(message_args_values), raw_message)

        message_args = {}
        for i in range(len(message_args_names)):
            message_args[message_args_names[i]] = message_args_values[i]

        return Message(message_type, raw_message, message_args)


    @staticmethod
    def __pack_message(mtype, args: dict):
        raw_message = mtype.value.build(args)
        return Message(mtype, raw_message, args)


    @staticmethod
    def pack_hash_assignment(hash_key: str):
        return MessageParser.__pack_message(mt.MessageType.ASSIGN_HASH, {'hash_key': hash_key})


    @staticmethod
    def pack_hash_result_report(hash_key: str, hash_result: str):
        return MessageParser.__pack_message(mt.MessageType.REPORT_RESULT, {'hash_key': hash_key, 'hash_result': hash_result})


    @staticmethod
    def pack_performance_request():
        return MessageParser.__pack_message(mt.MessageType.REQUEST_PERFORMANCE, {})


    @staticmethod
    def pack_performance_report(CPUPerformance: CPUPerformance):
        args = {
            'cores': CPUPerformance.get_cores(),
            'frequency': CPUPerformance.get_frequency(),
            'utilization': CPUPerformance.get_utilization()
        }
        return MessageParser.__pack_message(mt.MessageType.REPORT_PERFORMANCE, args)


    @staticmethod
    def pack_hash_results_request():
        return MessageParser.__pack_message(mt.MessageType.REQUEST_RESULTS, {})


    @staticmethod
    def cpu_performance_from_message(message):
        args = message.get_args()
        return CPUPerformance.CPUPerformance(args['cores'], args['frequency'], args['utilization'])


class ParseError(Exception):
    def __init__(self, parse_error, raw_message):
        super().__init__(f'Parsing of {parse_error} failed - {raw_message}')


class InvalidNumberOfArguments(ParseError):
    def __init__(self, number_of_raw_arguments, number_of_actual_arguments, raw_message):
        super().__init__(f'number of required arguments - {number_of_raw_arguments} but received - {number_of_actual_arguments} arguments.', raw_message)
