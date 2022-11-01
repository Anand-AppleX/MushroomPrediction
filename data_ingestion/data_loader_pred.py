import pandas as pd
from logger import logging

class Data_getter:

    """This class help to load data from Training_FileFromDB"""


    def __init__(self):

        self.path = 'Prediction_database/InputFile.csv'
        self.logger = logging

    def load_data(self):

        try:
            self.logger.info('{} LOADING DATA {}'.format('='*20,'='*20))

            self.data = pd.read_csv(self.path)

            self.logger.info("{} DATA READED SUCCESSFULLY {}".format('='*20,'='*20))

            return self.data


        except Exception as e:

            self.logger.info('Error ouccer during reading data from Training_FileFromDB is : '+ str(e))