import abc

class AnomalyDetector(object):
    """
    Base class for all anomaly detectors. When inheriting from this class please
    take note of which methods MUST be overridden, as documented below.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, filename, values, labels, proportion):
        """
        filename: time-series data filename
        dataSet(values & labels): a list of an ordered time-series data(Timestamp is continuous)
        proportion: training_length / total_length
        For example, there are 2000 elements(timestamps) in data_set and proportion is 0.6. 
        Then the first 2000*0.6 = 1200 will be used for training and the left 800 elements will be in testing.
        """
        self.filename = filename
        self.values = values
        self.labels = labels
        self.proportion = proportion
    
    def initialize(self):
        """
        Do anything you like to initialize your detector
        """
        pass

    @abc.abstractmethod
    def trainPhase(self, front_values, front_labels):
        """
        This method MUST be overridden by subclasses.
        Input values and abnormal labels, you may train your model during this phase.
        """
        assert False
    
    @abc.abstractmethod
    def isAnomaly(self, value):
        """
        This method MUST be overridden by subclasses.
        You need to return an integer 0(normal) or 1(abnormal)
        """
        assert False

    def __detectPhase(self, latter_values):
        """
        Note: Returned list should have the same length with 'values'.
        """
        return map(self.isAnomaly, latter_values)
    
    def run(self):
        """
        Main function that is called to collect anomaly detection results for a given file.
        """
        values_length = self.values.__len__()
        labels_length = self.labels.__len__()
        front_length = int(values_length * self.proportion)
        latter_length = values_length - front_length

        _front_values = self.values[:front_length]
        _latter_values = self.values[0-latter_length:]
        _front_labels = []
        for i in self.labels:
            if i < front_length:
                _front_labels.append(i)
        
        self.trainPhase(_front_values, _front_labels)

        # results_0_1 is a list that consists of either 0(normal) or 1(abnormal)
        results_0_1 = self.__detectPhase(_latter_values)
        # print results_0_1

        results_index= []
        for i, boo in enumerate(results_0_1):
            if boo == 1:
                results_index.append(i+front_length)

        return results_index
