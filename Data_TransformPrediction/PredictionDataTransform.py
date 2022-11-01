from datetime import datetime
from os import listdir
import pandas 
from logger import logging
import numpy as np
class dataTransform:

    def __init__(self):
        self.goodDataPath = "Prediction_Raw_files_validated/Good_Raw"
        self.logger = logging

    def doblecomma(self):

        " taking string from string"

        try:
            self.logger.info('{} seprating comma {}'.format('='*20,'='*20))

            onlyfile = [file for file in listdir(self.goodDataPath)]

            for file in onlyfile:
                csv = pandas.read_csv(self.goodDataPath+"/" + file)
                for i in csv.columns:
                    l = []
                    for j in csv[i]:
                        if len(j)>1:
                            l.append(j[1])
                        else:
                            l.append(j)
                    csv[i] = l

                csv.to_csv(self.goodDataPath+ "/" + file, index=None, header=True)
            self.logger.info('{} Done Successfully {}'.format('='*20,'='*20))

        except Exception as e:

            self.logger.ERROR('Error during comma sep value is : ' + str(e))
                


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

            self.logger.ERROR('Error during replacing missing value by nan is : ' + str(e))


    def addfile(self):

        self.logger.info('{} Adding file to one {}'.format('='*20,'='*20))

        onlyfile = [file for file in listdir(self.goodDataPath)]

        df = pandas.read_csv(self.goodDataPath + '/' + onlyfile[0])

        df.columns = ['cap-shape', 'cap-surface', 'cap-color', 'bruises', 'odor',
       'gill-attachment', 'gill-spacing', 'gill-size', 'gill-color',
       'stalk-shape', 'stalk-root', 'stalk-surface-above-ring',
       'stalk-surface-below-ring', 'stalk-color-above-ring',
       'stalk-color-below-ring', 'veil-type', 'veil-color', 'ring-number',
       'ring-type', 'spore-print-color', 'population', 'habitat']

        for i in onlyfile[1:]:
        
            df = df
            df1 = pandas.read_csv(self.goodDataPath + '/' + i)

            df1.columns = ['cap-shape', 'cap-surface', 'cap-color', 'bruises', 'odor',
        'gill-attachment', 'gill-spacing', 'gill-size', 'gill-color',
        'stalk-shape', 'stalk-root', 'stalk-surface-above-ring',
        'stalk-surface-below-ring', 'stalk-color-above-ring',
        'stalk-color-below-ring', 'veil-type', 'veil-color', 'ring-number',
        'ring-type', 'spore-print-color', 'population', 'habitat']
        
            df = pandas.concat([df,df1],ignore_index=False)

        df.to_csv(self.goodDataPath + '/' + 'mushroomMain_02034068_000001.csv',index=False)

        self.logger.info('Adding of csv done')