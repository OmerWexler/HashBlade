import psutil
import os
from .CPUPerformance import CPUPerformance
import logging

class PerformanceCalculator:
    __CPU_UTILIZATION_POLL_INTERVAL = 0.5
    __CPU_UTILIZATION_POLL_TIMES = 10


    def analyze_cpu_performance(self):
        
        cores = self.get_cpu_count()
        freq = self.get_cpu_frequency()
        utilization = self.get_cpu_utilization()
        
        logging.debug(f'Raw:\nCores - {cores}, utilization - {utilization}, freq - {freq}')

        return CPUPerformance(cores, freq, utilization)
        

    def get_cpu_count(self):
        return psutil.cpu_count()


    def get_cpu_frequency(self):
        return psutil.cpu_freq()[0]


    def get_cpu_utilization(self, debug=False):
        utilization = 0.0
        for i in range(0, self.__CPU_UTILIZATION_POLL_TIMES):
            utilization += psutil.cpu_percent(self.__CPU_UTILIZATION_POLL_INTERVAL) / self.__CPU_UTILIZATION_POLL_TIMES
            logging.debug(f'Polling cpu utilization - {utilization}')
        
        return utilization / 100.0