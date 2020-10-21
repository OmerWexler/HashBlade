from .MessageParser import MessageParser
from .MessageType import MessageType

print('Message parser:')
msg_format = MessageParser.generate_format(00, ['arg1', 'arg2'])
print(msg_format)
print(msg_format.format(arg1='value1', arg2='value2'))

msg_format = MessageParser.generate_format(00, [])
print(msg_format)

print('\n\nMessage type:')
for mtype in MessageType:
    print(f'{mtype} - {mtype.value}')

print('\n\nMessage build:')
m = MessageType.ASSIGN_HASH.value
print(m.format(**{'hash_key': 1111}))