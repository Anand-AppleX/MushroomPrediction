from datetime import datetime
from os import listdir
import pandas
from logger import logging
import numpy as np
class dataTransform:

    def __init__(self):
        self.goodDataPath = "Training_Raw_files_validated/Good_Raw"
        self.logger = logging

    def replaceMissingWithNull(self):

        """replacing ? with np.Nan"""
        try:

            self.logger.info('{} Replacing missing with  nan {}'.format('='*20,'='*20))

            onlyfile = [file for file in listdir(self.goodDataPath)]

            for file in onlyfile:

                csv = pandas.read_csv(self.goodDataPath+"/" + file)

                for i in csv.columns:
                    l = []
                    for j in csv[i]:
                        if j == '?':
                            l.append(np.NaN)
                        else:
                            l.append(j)
                    csv[i] = l

                csv.to_csv(self.goodDataPath+ "/" + file, index=None, header=True)
                p = []
                for i in csv.columns:
                    if csv[i].isnull().sum() >= 1:
                        s = csv[i].isnull().sum()
                        p.append(i + ' : ' +str(s))
                    else:
                        pass
                self.logger.info('{} has nan value added'.format(p))
                self.logger.info('{}File appended to good folder{}'.format('='*20,'='*20))
            
        except Exception as e:

            self.logger.info('Error during replacing missing value by nan is : ' + str(e))