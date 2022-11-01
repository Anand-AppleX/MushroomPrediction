from logger import logging
from TrainingDataValidation import trainingdatavalidation
from Training_database_Connection import trainingDB 
from Data_TransformTraining import DataTransformation
from datetime import datetime

class train_validation:

    def __init__(self,path):
        self.logger = logging

        self.path = path

    def trainValidation(self):

        """"Doing full validation"""

        try:

            s = trainingdatavalidation.training_validation(self.path)

            NumberOfColumn,Column_name = s.valuesfromschema()

            regex = s.makingregex()

            s.validatingnameofFile(regex)

            s.validatingColumnLength(NumberOfColumn)
            
            s.validateMissingValuesInWholeColumn()

            self.logger.info('{} Validation completed {}'.format('='*20,'='*20))

            DataTransformation.dataTransform().replaceMissingWithNull()

            self.logger.info('{} transformation done completed {}'.format('='*20,'='*20))

            self.logger.info('{} DataBase Starting {}'.format('='*20,'='*20))

            trainingDB.DBOperation().loadtodatabase()

            trainingDB.DBOperation().selectingfromdatabase()

            self.logger.info('{} DataBase Done File Loaded {}'.format('='*20,'='*20))

            s.movingBadDirectoryToArchived()

        except Exception as e:

            self.logger.info('Error in training_validation is : ' + str(s))
            


