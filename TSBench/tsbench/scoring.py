try:
  import simplejson as json
except ImportError:
  import json
import os

def sOld(t_labels, detected, f_length, l_length):
    (TP, TN, FP, FN) = (0, 0, 0, 0)
    a_length = f_length + l_length
    for id in xrange(f_length, a_length):
        x1 = id in t_labels
        x2 = id in detected
        if x1 and x2:
            TP += 1
        elif not x1 and x2:
            FP += 1
        elif x1 and not x2:
            FN += 1
        else:
            TN += 1
    return (TP, TN, FP, FN)

def sPei_New(delay, pei_new, t_labels, detected, f_length, l_length):
    (TP, TN, FP, FN) = (0, 0, 0, 0)
    a_length = f_length + l_length
    id = f_length
    while id < a_length:
        anomaly_duration = 0
        while id + anomaly_duration in t_labels:
            anomaly_duration += 1
        right_most = id + min(anomaly_duration, delay+1)
        flag = 0
        for t in xrange(id, right_most):
            if t in detected:
                flag = 1
                break
        if flag == 1: # all -> 1 (TP)
            if pei_new == 'pei':
                TP += anomaly_duration
            else:
                TP += 1
        elif anomaly_duration > 0: # all -> 0 (FN)
            if pei_new == 'pei':
                FN += anomaly_duration
            else:
                FN += 1
        else: # This is not an anomaly
            if id in detected:
                FP += 1
            else:
                TN += 1
        id += max(1, anomaly_duration)
    
    return (TP, TN, FP, FN)

def score(scoring_name, delay, t_labels, detected, f_length, l_length):
    """
    @param scoring_name (str) name of scoring scheme
    @param delay    (int)  non-negative number
    @param t_labels (list) true anomaly-index labels
    @param detected (list) detected labels by specific algorithm
    @param f_length (int)  training data length
    @param l_length (int)  test data length
    """
    if scoring_name == 'old':
        return sOld(t_labels, detected, f_length, l_length)
    elif scoring_name == 'new':
        return sPei_New(delay, 'new', t_labels, detected, f_length, l_length)
    else:
        return sPei_New(delay, 'pei', t_labels, detected, f_length, l_length)


def addTogether(score_json_path):
    source_data = {}
    with open(score_json_path) as f:
        source_data = json.load(f)
    
    results = {}
    results['total'] = [0, 0, 0, 0, 0, 0, 0]
    # accumulate TP, TN, FP, FN
    for key in source_data:
        csv_file_name_len = key.split('/')[-1].__len__()
        x = key[:0 - csv_file_name_len]
        if x not in results:
            results[x] = [0, 0, 0, 0, 0, 0, 0] # TP, TN, FP, FN, Precision, Recall, FScore
        for ii in xrange(4): # accumulate TP, TN, FP, FN
            results[x][ii] = results[x][ii] + source_data[key][ii]
            results['total'][ii] = results['total'][ii] + source_data[key][ii]
    
    # calculate Precision, Recall and F-Score
    for r in results:
        try:
            results[r][4] = (results[r][0] + 0.0) / (results[r][0] + results[r][2] + 0.0)  # Precision = TP/(TP + FP)
            results[r][5] = (results[r][0] + 0.0) / (results[r][0] + results[r][3] + 0.0)  # Recall = TP/(TP + FN)
            results[r][6] = round(2 * results[r][4] * results[r][5] / (results[r][4] + results[r][5]), 4)
            results[r][4] = round(results[r][4], 4)
            results[r][5] = round(results[r][5], 4)
        except ZeroDivisionError:
            results[r][4], results[r][5], results[r][6] = 0.0, 0.0, 0.0
        
    return results


if __name__ == '__main__':
    r = addTogether('./results/random/scoreTraditional.json')
    for k in r:
        print k, r[k]
        print ''
