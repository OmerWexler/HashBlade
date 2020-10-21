from .Utils import Utils
from communication import Message

class CPUPerformance:
    def __init__(self, cores, frequency, utilization, overall=None):
        self.__cores = cores
        self.__frequency = frequency
        self.__utilization = utilization
        self.__overall = overall


    def get_cores(self):
        return self.__cores


    def get_frequency(self):
        return self.__frequency


    def get_utilization(self):
        return self.__utilization


    def get_overall(self):
        return self.__overall
    

    def __str__(self):
        return f'Scaled:\nCores - {self.__cores}, utilization - {self.__utilization}, freq - {self.__frequency}, overall {self.__overall}'