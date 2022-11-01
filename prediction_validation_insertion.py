from logger import logging
from PredictionDataValidation import  PredictionValidation
from Data_TransformPrediction.PredictionDataTransform import  dataTransform
from Prediction_Database_connection.predictionDB import DBOperationPre
from datetime import datetime

class pred_validation:

    def __init__(self,path):
        self.logger = logging

        self.path = path

    def PredValidation(self):

        """"Doing full validation"""

        try:

            s = PredictionValidation.Prediction_Data_validation(self.path)

            LengthOfDateStampInFile,LengthOfTimeStampInFile,column_names,noofcolumns = s.valuesFromSchema()

            regex = s.manualRegexCreation()

            s.validationFileNameRaw(regex,LengthOfDateStampInFile,LengthOfTimeStampInFile)

            s.validatingColumnLength(noofcolumns)
            
            s.validateMissingValuesInWholeColumn()

            self.logger.info('{} Prediction Validation completed {}'.format('='*20,'='*20))
            dataTransform().doblecomma()

            dataTransform().replaceMissingWithNull()

            dataTransform().addfile()

            self.logger.info('{} transformation done completed {}'.format('='*20,'='*20))

            self.logger.info('{} DataBase Starting {}'.format('='*20,'='*20))

            DBOperationPre().Preloadtodatabase()
            DBOperationPre().selectingfromdatabase()

            self.logger.info('{} DataBase Done File Loaded {}'.format('='*20,'='*20))

            s.movingBadDirectoryToArchived()

            self.logger.info('{} Prediction Validation Completed {}'.format('='*20,'='*20))

        except Exception as e:

            self.logger.info('Error in Prediction_validation is : ' + str(e))

            raise e



