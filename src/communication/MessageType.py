from enum import Enum, unique

@unique
class MessageType(Enum):
    REQUEST_PERFORMANCE = 0,
    REPORT_PERFORMANCE = 1,
    ASSIGN_HASH = 2,
    REQUEST_RESULT = 3,
    REPORT_RESULT = 4