import os
import helper
import scoring
from tsbench.algorithms.knncad.knncad_detector import KnncadDetector as selectedDetector
try:
    import simplejson as json
except ImportError:
  import json
from multiprocessing import Pool

anomaly_results = {}

def detectSingle(k, value, label, proportion):
    """ k is filename. """
    sd = selectedDetector(k, value, label, proportion)
    result = sd.run() # return index of detected abnormal points
    return (k, result)

def collect_results(data):
    global anomaly_results
    anomaly_results[data[0]] = data[1]


def detect(values, labels, proportion):
    """ execute self-defined detectors"""
    p = Pool()        
    for k in values:
        p.apply_async(detectSingle, (k, values[k], labels[k], proportion), callback=collect_results)
    p.close()
    p.join()


def detectResultToFile(algorithm):
    result_dir = './results/' + algorithm + '/'
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    json_path = result_dir + 'anomaly_points.json'

    with open(json_path, 'w') as f:
        global anomaly_results
        json.dump(anomaly_results, f, indent=4)


def scoreAndWriteResult(labels, values, proportion, algorithm, scoring_name, delay):
    scores = {}
    for d in labels:
        front_length = int(values[d].__len__() * proportion)
        latter_length = values[d].__len__() - front_length
        global anomaly_results
        (TP, TN, FP, FN) = scoring.score(scoring_name, delay, labels[d], anomaly_results[d], front_length, latter_length)  
        try:
            Precision = (TP + 0.0) / (TP + FP + 0.0)
            Recall = (TP + 0.0) / (TP + FN + 0.0)
            FScore = 2 * Precision * Recall / (Precision + Recall)
        except ZeroDivisionError:
            Precision, Recall, FScore = 0.0, 0.0, 0.0
        
        scores[d] = (TP, TN, FP, FN, Precision, Recall, FScore)
        
    json_path = './results/' + algorithm + '/score_' + scoring_name + '.json'
    with open(json_path, 'w') as f:
        json.dump(scores, f, indent=4)
    

def saveProportion(algorithm, proportion):
    with open('./results/{0}/proportion.txt'.format(algorithm), 'w') as f:
        f.write(str(proportion))


def execute(algorithm, proportion, scoring, delay):
    values = helper.getData()   # dict
    labels = helper.getLabels() # dict
    detect(values, labels, proportion)
    detectResultToFile(algorithm)
    print 'detect successfully done.\nwriting results to file'
    scoreAndWriteResult(labels, values, proportion, algorithm, scoring, delay)
    saveProportion(algorithm, proportion)
