# This script is used for reading source data and labels
import os
import csv
try:
  import simplejson as json
except ImportError:
  import json


def getAllFilePaths(root_path='./data/'):
    results = []
    dirs = os.listdir(root_path) # root_path = './data/'
    for d in dirs:
        d = root_path + d
        if os.path.isdir(d):
            _csv_files = os.listdir(d)
            for cf in _csv_files:
                if cf[-4:] == '.csv':
                    results.append(d + '/' + cf)
        else:
            pass
    return results


def getSingleData(file_path):
    results = []
    with open(file_path, 'r') as f:
        rows = csv.reader(f)
        i = 0
        for r in rows:
            if i > 0:
                results.append(float(r[1]))
            else:
                i = 1
    return results

def getData(root_path='./data/'):
    """
    return a dictionary. 
    key: file_path
    value: time-series data
    """
    data_dict = {}
    afp = getAllFilePaths(root_path)
    for fp in afp:
        data_dict[fp] = getSingleData(fp)
    return data_dict


def getLabels(labels_file_path='./data/labels.json'):
    with open(labels_file_path) as f:
        return json.load(f)


if __name__ == '__main__':
    print getSingleData('E:/TSBench/data/dir_1/1_1.csv')