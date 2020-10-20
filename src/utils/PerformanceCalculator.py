import psutil
import os
from .Utils import Utils
from .CPUPerformance import CPUPerformance

class PerformanceCalculator:
    __CPU_UTILIZATION_POLL_INTERVAL = 0.5
    __CPU_UTILIZATION_POLL_TIMES = 10


    def __init__(self, inject_cores=None, inject_frequency=None, inject_utilization=None):
        self.__inject_cores = inject_cores
        self.__inject_frequency = inject_frequency
        self.__inject_utilization = inject_utilization


    def analyze_cpu_performance_relative(self, 
            core_counts=[2*2, 8*2],
            frequencies=[2400, 4600],
            debug=False):

        cpu_max_cores = None
        cpu_min_cores = None
        cpu_max_frequency = None
        cpu_min_frequency = None
        
        for count in core_counts:
            if cpu_max_cores == None or cpu_max_cores < count:
                cpu_max_cores = count
            
            if cpu_min_cores == None or cpu_min_cores > count:
                cpu_min_cores = count
        
        if debug:
            print(f'Max cores - {cpu_max_cores}, Min cores - {cpu_min_cores}')
        
        for count in frequencies:
            if cpu_max_frequency == None or cpu_max_frequency < count:
                cpu_max_frequency = count
            
            if cpu_min_frequency == None or cpu_min_frequency > count:
                cpu_min_frequency = count
        
        if debug:
            print(f'Max frequency - {cpu_max_frequency}, Min frequency - {cpu_min_frequency}')


        return self.analyze_cpu_performance(            
            cpu_max_cores=cpu_max_cores, 
            cpu_min_cores=cpu_min_cores, 
            cpu_max_frequency=cpu_max_frequency, 
            cpu_min_frequency=cpu_min_frequency,
            debug=debug) 


    def analyze_cpu_performance(self, 
            cpu_max_cores=8*2, 
            cpu_min_cores=2*2,
            cpu_max_frequency=4600, 
            cpu_min_frequency=2400,
            cpu_max_utilization = 100,
            cpu_min_utilization = 0, 
            debug=False):
        
        cores = self.get_cpu_count()
        freq = self.get_cpu_frequency()
        utilization = self.get_cpu_utilization(debug=debug) 

        scaled_cores = Utils.scale(cores, cpu_min_cores, cpu_max_cores) 
        scaled_freq = Utils.scale(freq, cpu_min_frequency, cpu_max_frequency)
        scaled_util = Utils.scale(utilization, cpu_min_utilization, cpu_max_utilization, True)

        if debug:
            print(f'Raw:\nCores - {cores}, utilization - {utilization}, freq - {freq}')
            print(f'Scaled:\nCores - {scaled_cores}, utilization - {scaled_util}, freq - {scaled_freq}')

        return CPUPerformance(scaled_cores, scaled_freq, scaled_util)
        

    def get_cpu_count(self):
        if self.__inject_cores == None:
            return psutil.cpu_count()
        else:
            return self.__inject_cores


    def get_cpu_frequency(self):
        if self.__inject_frequency == None:
            return psutil.cpu_freq()[0]
        else:
            return self.__inject_frequency


    def get_cpu_utilization(self, debug=False):
        if self.__inject_utilization == None:
            utilization = 0.0
            for i in range(0, self.__CPU_UTILIZATION_POLL_TIMES):
                utilization += psutil.cpu_percent(self.__CPU_UTILIZATION_POLL_INTERVAL) / self.__CPU_UTILIZATION_POLL_TIMES
                if debug:
                    print(f'Polling cpu utilization - {utilization}')
            
            return utilization
        else:
            return self.__inject_utilization