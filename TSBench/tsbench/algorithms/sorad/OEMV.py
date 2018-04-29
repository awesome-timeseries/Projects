class OEMV(object):
    """ Online Estimation of sample Mean and Variance """
    def __init__(self, forgetting_factor):
        self.__inited = 0
        self.__lambda = forgetting_factor
        self.__sigma = 0
        self.__mean = 0
        self.__H = 0
        self.__Q = 0
        self.__M = 0
        self.__variance = 0

    def update(self, new_data):
        if self.__inited == 1:
            self.__sigma = self.__lambda * self.__sigma + 1
            self.__mean = self.__mean + (new_data - self.__mean) / self.__sigma
            self.__H = self.__lambda * self.__H + new_data ** 2
            self.__Q = self.__lambda * self.__Q + new_data
            self.__M = self.__H - 2 * self.__mean * self.__Q
            self.__variance = self.__M / self.__sigma + self.__mean ** 2
        else:
            self.__inited = 1
            self.__sigma = 1
            self.__mean = new_data
            self.__H = new_data ** 2
            self.__Q = new_data
            self.__M = - new_data ** 2
    
    def getMeanSD(self):
        """return mean and standard variance"""
        return (self.__mean, self.__variance**0.5)

