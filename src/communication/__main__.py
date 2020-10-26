from .MessageParser import MessageParser
from .MessageType import MessageType
from .MessageFormat import MessageFormat
from utils import CPUPerformance


print('Message format:')
msg_format = MessageFormat(00, ['arg1', 'arg2']).get_raw_format()
print(msg_format)
print(msg_format.format(arg1='value1', arg2='value2'))

msg_format = MessageFormat(00, []).get_raw_format()
print(msg_format)

print('\n\nMessage type:')
for mtype in MessageType:
    print(f'{mtype} - {mtype.value.get_mid()}')

# print('\n\nMessage build:')
#  m = MessageType.ASSIGN_HASH.value.format(**{'hash_key': 1111})
# print(m)

# print('\n\nParse:')
# m = MessageParser.parse_message(m)
# print(m)

# print('\n\nAssign Hash Pack:')
# m = MessageParser.pack_hash_assignment('1124')
# print(m)

# print('\n\nResult report:')
# m = MessageParser.pack_hash_result_report('1124', '4211')
# print(m)

# print('\n\nRequest result:')
# m = MessageParser.pack_hash_results_request()
# print(m)

# print('\n\nPerformance request:')
# m = MessageParser.pack_performance_request()
# print(m)

# print('\n\nAssign Hash Pack:')
# m = MessageParser.pack_performance_report(CPUPerformance(2, 4000, 90))
# print(m)