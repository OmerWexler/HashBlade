from .ClientCommunicator import ClientCommunicator
from communication import MessageParser
from utils import PerformanceCalculator

cc = ClientCommunicator('127.0.0.1', 6400)
cc.connect()
cc.accept_message()
cc.report_performance(PerformanceCalculator().analyze_cpu_performance())