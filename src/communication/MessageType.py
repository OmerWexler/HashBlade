from enum import Enum, unique

import communication.MessageParser as mp

@unique
class MessageType(Enum):
    REQUEST_PERFORMANCE = mp.MessageParser.generate_format(0, [])
    REPORT_PERFORMANCE = mp.MessageParser.generate_format(1, ['cores', 'frequency', 'utilization'])
    ASSIGN_HASH = mp.MessageParser.generate_format(2, ['hash_key'])
    REPORT_RESULT = mp.MessageParser.generate_format(4, ['hash_key', 'hash_result'])
    REQUEST_RESULTS = mp.MessageParser.generate_format(3, [])


    @staticmethod
    def translate_from_id(mid: int):
        mid = str(mid).zfill(2)
        
        for mtype in MessageType:
            if mtype.value.startswith(mid):
                return mtype
        
        raise MessageTypeDoesntExist(mid)


class MessageTypeDoesntExist(Exception):
    def __init__(self, mid):
        super().__init__(f'Message id - {mid} doesn\'t exist.')