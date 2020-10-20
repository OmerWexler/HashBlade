from .Utils import Utils

class CPUPerformance:
    def __init__(self, cores, frequency, utilization):
        self.cores = cores
        self.frequency = frequency
        self.utilization = utilization
        self.overall = Utils.scale(self.cores * self.frequency * self.utilization, 0.0, 1.0)

    def __str__(self):
        return f'Scaled:\nCores - {self.cores}, utilization - {self.utilization}, freq - {self.frequency}, overall {self.overall}'