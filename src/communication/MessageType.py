from enum import Enum, unique

# from .MessageParser import MessageParser
import communication.MessageParser as mp

@unique
class MessageType(Enum):
    REQUEST_PERFORMANCE = mp.MessageParser.generate_format(0, [])
    REPORT_PERFORMANCE = mp.MessageParser.generate_format(1, ['cores', 'freqeuncy', 'utilization'])
    ASSIGN_HASH = mp.MessageParser.generate_format(2, ['hash_key'])
    REPORT_RESULT = mp.MessageParser.generate_format(4, ['hash_key', 'hash_result'])
    REQUEST_RESULTS = mp.MessageParser.generate_format(3, [])