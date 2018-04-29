def adjust(algorithm_name):
    path_ = './tsbench/runner.py'
    with open(path_, 'r') as f:
        data = f.readlines()
    data[3] = 'from tsbench.algorithms.'+algorithm_name+'.'+algorithm_name+'_detector import '+ algorithm_name.capitalize()+'Detector as selectedDetector\n'
    with open(path_, 'w') as f:
        f.writelines(data)

if __name__ == '__main__':
    adjust('random')
