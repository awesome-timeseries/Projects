from tsbench.algorithms.base import AnomalyDetector
import numpy as np
import math

class KnncadDetector(AnomalyDetector):
    """
    This detector is originated from a paper "Conformalized density- and
    distance-based anomaly detection in time-series data" by E.V.Burnaev et.al.
    """
    def __init__(self, *args, **kwargs):
        super(KnncadDetector, self).__init__(*args, **kwargs)
        self.buf = []
        self.training = []
        self.calibration = []
        self.scores = []
        self.record_count = 0
        self.k = 5
        self.dim = 5
        self.sigma = np.diag(np.ones(self.dim))
        self.traingLength = 500

    def metric(self,a,b):
        diff = a-np.array(b)
        return np.dot(np.dot(diff,self.sigma),diff.T)

    def ncm(self,item, item_in_array=False):
        arr = map(lambda x:self.metric(x,item), self.training)
        return np.sum(np.partition(arr, self.k+item_in_array)[:self.k+item_in_array])

    def trainPhase(self, front_values, front_labels):
        for fv in front_values:
            x = self._isAnomaly(fv)
    
    def isAnomaly(self, value):
        return self._isAnomaly(value)

    def _isAnomaly(self, value):
        self.buf.append(value)
        self.record_count += 1
        
        if len(self.buf) < self.dim:
            return 0
        else:
            new_item = self.buf[-self.dim:]
            if self.record_count < self.traingLength:
                self.training.append(new_item)
                return 0
            else:
                ost = self.record_count % self.traingLength
                if ost == 0 or ost == int(self.traingLength/2):
                    try:
                        self.sigma = np.linalg.inv(np.dot(np.array(self.training).T, self.training))
                    except np.linalg.linalg.LinAlgError:
                        print 'Singular Matrix at record', self.record_count 
                if len(self.scores) == 0:
                    self.scores = map(lambda v: self.ncm(v, True), self.training)
                    
                new_score = self.ncm(new_item)
                result = 1.*len(np.where(np.array(self.scores) < new_score)[0])/len(self.scores)
                
                if self.record_count >= 2*self.traingLength:
                    self.training.pop(0)
                    self.training.append(self.calibration.pop(0))
                
                self.scores.pop(0)    
                self.calibration.append(new_item)
                self.scores.append(new_score)
                
                if result > 0.99:
                    return 1
                else:
                    return 0
