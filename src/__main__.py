import sys
import argparse

from client import Client
from server import Server
from communication import Message, MessageType

parser = argparse.ArgumentParser()
parser.add_argument('--type', choices=['server', 'client'], dest='type', required=True)
args = parser.parse_args(sys.argv[1:3])

if args.type == 'server':
    server = Server(sys.argv[3:])
    server.init()
elif args.type == 'client':
    client = Client(sys.argv[3:])
    client.init()