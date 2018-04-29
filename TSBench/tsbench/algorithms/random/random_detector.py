import random
from tsbench.algorithms.base import AnomalyDetector

class RandomDetector(AnomalyDetector):
    """
    A simple random detector
    """
    def __init__(self, *args, **kwargs):
        super(RandomDetector, self).__init__(*args, **kwargs)
        
    def trainPhase(self, front_values, front_labels):
        self.rate = (front_labels.__len__() + 0.0) / (front_values.__len__() + 0.0)

    def isAnomaly(self, value):
        if random.uniform < self.rate:
            return 1
        else:
            return 0

if __name__ == '__main__':
    pass
