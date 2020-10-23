from enum import Enum, unique
import communication.MessageFormat as mf


@unique
class MessageType(Enum):
    REQUEST_PERFORMANCE = mf.MessageFormat(0, [])
    REPORT_PERFORMANCE = mf.MessageFormat(1, ['cores', 'frequency', 'utilization'])
    ASSIGN_HASH = mf.MessageFormat(2, ['hash_key'])
    REQUEST_RESULTS = mf.MessageFormat(3, [])
    REPORT_RESULT = mf.MessageFormat(4, ['hash_key', 'hash_result'])


    @staticmethod
    def translate_from_id(mid: int):
        mid = str(mid).zfill(2)
        
        for mtype in MessageType:
            if mtype.value.get_mid() == mid:
                return mtype
        
        raise MessageTypeDoesntExist(mid)


class MessageTypeDoesntExist(Exception):
    def __init__(self, mid):
        super().__init__(f'Message id - {mid} doesn\'t exist.')