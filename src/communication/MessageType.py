from enum import Enum, unique
import communication.MessageFormat as mf


class MessageType(Enum):
    REQUEST_PERFORMANCE = mf.MessageFormat(0, [])
    REPORT_PERFORMANCE = mf.MessageFormat(1, ['cores', 'frequency', 'utilization'])
    ASSIGN_HASH = mf.MessageFormat(2, ['range_start', 'range_end'])
    REQUEST_RESULTS = mf.MessageFormat(3, ['hash_target'])
    REPORT_RESULT = mf.MessageFormat(4, ['range_start', 'range_end', 'hash_result'])
    KILL = mf.MessageFormat(5, [])


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