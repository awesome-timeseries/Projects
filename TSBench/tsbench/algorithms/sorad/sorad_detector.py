from tsbench.algorithms.base import AnomalyDetector
from OEMV import OEMV
import math
import numpy as np
from numpy.linalg import LinAlgError
from scipy import stats
try:
    import simplejson as json
except ImportError:
  import json


class SoradDetector(AnomalyDetector):
    """
    This detector is an implementation of Algorithm 2(SORAD) in 
    "Online Anomaly Detection on the Webscope S5 Dataset: A Comparative Study"
    by Markus Thill et al.
    """
    def __init__(self, *args, **kwargs):
        super(SoradDetector, self).__init__(*args, **kwargs)
        """
        f_rls: forgetting factor of RLS
        f_ms: forgetting factor of "online estimation of sample mean and standard_deviation"
        threshold: anomaly threshold for calculating quantile
        window_size: use previous window_size points to predict next point
        """
        (self.f_rls, self.f_ms, self.threshold, self.ws) = self.initialize()
        (self.__P, self.theta) = None, None # will be initilied in trainPhase
        self.oemv = OEMV(self.f_ms)
        self.lastvalues = self.ws * [0.0] # keep updating
        
    def initialize(self):
        with open("./tsbench/algorithms/sorad/parameters.json") as f:
            data = json.load(f)
            param = data[self.filename]
            return (param['f_rls'], param['f_ms'], param['threshold'], param['ws'])

    def trainPhase(self, front_values, front_labels):
        (self.__P, self.theta) = self.initial(front_values[:self.ws+2])

        train_len = front_values.__len__()
        flag_ms = 0
        k = self.ws
        while k < train_len - 1:
            X_k = np.matrix([1] + [front_values[k-i] for i in xrange(self.ws)]).T
            predict_Y = self.theta.T * X_k
            prediction_error = front_values[k+1] - predict_Y.getA()[0][0] # Y_k+1 = front_values[k+1]
            if flag_ms < 4: # transient phase: 4 can be substituted by 3,5,6
                # update anyway(We assume there is no anomaly in transient phase)
                self.oemv.update(prediction_error)
                self.update_p_theta(prediction_error, X_k)
                flag_ms += 1
            else:
                (mean, sd) = self.oemv.getMeanSD()
                # mean = 0 calculate quantile
                z_epsilon = stats.norm(0, sd).ppf((1-self.threshold) / 2.0) # minus !!
                if mean + z_epsilon < prediction_error < mean - z_epsilon or z_epsilon < prediction_error < - z_epsilon: # normal
                    self.oemv.update(prediction_error)
                    self.update_p_theta(prediction_error, X_k)
                else: # abnormal(no updating operation)
                    k = k + self.ws
            k += 1
        
        # We need to record the last window-size values in training phase.
        self.lastvalues = front_values[-self.ws:] # we expect the last window-size values are normal.

    def isAnomaly(self, value):
        X_k = np.matrix([1] + self.lastvalues).T
        predict_Y = self.theta.T * X_k
        self.lastvalues.pop(0)

        prediction_error = value - predict_Y.getA()[0][0]
        (mean, sd) = self.oemv.getMeanSD()
        z_epsilon = stats.norm(0, sd).ppf((1-self.threshold) / 2.0) # minus !!
        if mean + z_epsilon < prediction_error < mean - z_epsilon or z_epsilon < prediction_error < - z_epsilon: # normal
            self.lastvalues.append(value)
            self.oemv.update(prediction_error)
            self.update_p_theta(prediction_error, X_k)
            return 0
        else:
            self.lastvalues.append(predict_Y)
            return 1

    def initial(self, beginning_ts):
        """ initialize matrix P and theta """
        u0 = np.matrix([1] + [beginning_ts[self.ws-i-1] for i in xrange(self.ws)])
        u1 = np.matrix([1] + [beginning_ts[self.ws-i] for i in xrange(self.ws)])
        try:
            P_matrix = np.linalg.inv(u0.T * u0 + self.f_rls * u1.T * u1)
        except LinAlgError:
            #print 'exception in P_matrix-initialization'
            P_matrix = np.eye(self.ws + 1)
        
        d0 = np.matrix(beginning_ts[self.ws])
        d1 = np.matrix(beginning_ts[self.ws+1])
        Z = u0.T * d0 + self.f_rls * u1.T * d1

        theta = P_matrix * Z

        return (P_matrix, theta)
    
    def update_p_theta(self, delta, X_k):
        """
        delta: prediction error (float)
        X_k: matrix(Nx1)
        """
        temp = 1.0 / (self.f_rls + (X_k.T * self.__P * X_k).getA()[0][0])
        self.__P = (self.__P - temp * self.__P * X_k * X_k.T * self.__P) / self.f_rls
        self.theta = self.theta + delta * self.__P * X_k


if __name__ == '__main__':
    pass
