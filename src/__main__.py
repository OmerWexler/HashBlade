import sys
import argparse

from client import Client
from server import Server
from communication import Message, MessageType
import logging


parser = argparse.ArgumentParser()
parser.add_argument('--type', choices=['server', 'client'], dest='type', required=True)
parser.add_argument('--log', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], dest='log', required=True)
args = parser.parse_args(sys.argv[1:5])

numeric_level = getattr(logging, args.log, None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)
logging.basicConfig(level=numeric_level)


if args.type == 'server':
    server = Server(sys.argv[5:])
    server.init()
elif args.type == 'client':
    client = Client(sys.argv[5:])
    client.init()