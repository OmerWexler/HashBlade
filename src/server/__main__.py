from .ServerCommunicator import ServerCommunicator
from communication import MessageParser


sc = ServerCommunicator('127.0.0.1', 6400)
sc.bind()
sc.accept_client()
sc.request_performance(0)
sc.accept_message(0)