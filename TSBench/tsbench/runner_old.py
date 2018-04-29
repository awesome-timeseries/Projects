import os
import helper
import scoring
from tsbench.algorithms.sorad.sorad_detector import SoradDetector as selectedDetector
try:
    import simplejson as json
except ImportError:
  import json


class Runner(object):
    def __init__(self, algorithm, proportion, scoring, delay):
        self.algorithm = algorithm       # str
        self.proportion = proportion     # float(0~1)
        self.scoring_name = scoring      # str
        self.delay = delay               # int(>=0)
        self.values = helper.getData()   # dict
        self.labels = helper.getLabels() # dict
        self.anomaly_results = self.detect()
    
    def detect(self):
        """ execute self-defined detectors"""
        results = {}
        i = 1
        for k in self.values:
            print k, 'detect done',
            for _ in xrange(i):
                print '.',
            print ''
            i += 1
            sd = selectedDetector(k, self.values[k], self.labels[k], self.proportion)
            results[k] = sd.run() # return index of detected abnormal point 
        return results

    def detectResultToFile(self):
        result_dir = './results/' + self.algorithm + '/'
        if not os.path.exists(result_dir):
            os.mkdir(result_dir)
        json_path = result_dir + 'anomaly_points.json'

        with open(json_path, 'w') as f:
            json.dump(self.anomaly_results, f, indent=4)
  
    def scoreAndWriteResult(self):
        scores = {}
        for d in self.labels:
            front_length = int(self.values[d].__len__() * self.proportion)
            latter_length = self.values[d].__len__() - front_length
            (TP, TN, FP, FN) = scoring.score(self.scoring_name, self.delay, self.labels[d], self.anomaly_results[d], front_length, latter_length)  
            try:
                Precision = (TP + 0.0) / (TP + FP + 0.0)
                Recall = (TP + 0.0) / (TP + FN + 0.0)
                FScore = 2 * Precision * Recall / (Precision + Recall)
            except ZeroDivisionError:
                Precision, Recall, FScore = 0.0, 0.0, 0.0
        
            scores[d] = (TP, TN, FP, FN, Precision, Recall, FScore)
        
        json_path = './results/' + self.algorithm + '/score_' + self.scoring_name + '.json'
        with open(json_path, 'w') as f:
            json.dump(scores, f, indent=4)
    
    def saveProportion(self):
        with open('./results/{0}/proportion.txt'.format(self.algorithm), 'w') as f:
            f.write(str(self.proportion))

    def execute(self):
        # to be done
        self.detectResultToFile()
        print 'detect successfully done.\nwriting results to file'
        self.scoreAndWriteResult()
        self.saveProportion()
