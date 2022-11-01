import os
from logger import logging
import json
import shutil
import re
from os import listdir
from datetime import datetime
import pandas as pd

class Prediction_Data_validation:

    def __init__(self,path):
        self.Batch_Directory = path
        self.schema = 'schema_prediction.json'
        self.logger = logging

    def valuesFromSchema(self):

        self.logger.info("======================VALUE FROM SCHEMA PATH======================")

        try:

            with open(self.schema,'r') as f:
                dic = json.load(f)
                f.close()

            Samplefilename = dic['SampleFileName']

            LengthOfDateStampInFile = dic['LengthOfDateStampInFile']

            LengthOfTimeStampInFile = dic['LengthOfTimeStampInFile']
            column_names = dic['ColName']
            NumberofColumns = dic['NumberofColumns']

            self.logger.info("SampleFileName is {} number of columns is {} LengthOfDateStampInFile {} LengthOfTimeStampInFile {} ".format(Samplefilename,NumberofColumns,LengthOfDateStampInFile,LengthOfTimeStampInFile))

            return LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, NumberofColumns

        except ValueError:

            self.logger.info('Error occured is : {}'.format(ValueError))

            raise ValueError

        except KeyError:

            self.logger.info('Error occured is : {}'.format(KeyError))
            raise KeyError

        except Exception as e :

            self.logger.info('Error occured is : ' + str(e))

            raise e


    def manualRegexCreation(self):

        regex = "['mushroom']+['\_'']+[\d_]+[\d]+\.csv"
        return regex


    def creatingDirectoryForGoodBadRawData(self):

        """This will create Good and Bad directory """

        try:
            path = os.path.join("Prediction_Raw_files_validated/", "Good_Raw/")
            if not os.path.isdir(path):
                os.makedirs(path)

            self.logger.info('{} Making Prediction_Raw_files_validated {}'.format('='*20,'='*20))

            path = os.path.join("Prediction_Raw_files_validated/", "Bad_Raw/")

            if not os.path.isdir(path):

                os.makedirs(path)
            self.logger.info('{} Making Prediction_Raw_files_validated done {}'.format('='*20,'='*20))


        except OSError:

            self.logger.info('Error occured is : ' + str(OSError))

            raise OSError


    def DeletingDirectoryForBadRawData(self):

        """ This class will delete bad directory  """
        try:

            path = "Prediction_Raw_files_validated/"

            if os.path.isdir(path + 'Bad_Raw/'):

                shutil.rmtree(path + 'Bad_Raw/')

                self.logger.info('{} Deleted BAD Directory {}'.format('='*20,'='*20))

        except OSError as s:

            self.logger.info('Error while deleting bad directory is : ' + str(s))

    def DeletingDirectoryForGoodRawData(self):

        """ This class will delete bad directory  """
        try:

            path = "Prediction_Raw_files_validated/"

            if os.path.isdir(path + 'Good_Raw/'):

                shutil.rmtree(path + 'Good_Raw/')

                self.logger.info('{} Deleted GOOD Directory {}'.format('='*20,'='*20))

        except OSError as s:

            self.logger.info('Error while deleting GOOd directory is : ' + str(s))


    def movingBadDirectoryToArchived(self):

        now = datetime.now()
        date = now.date()
        time = now.strftime("%H%M%S")

        try:

            source = 'Prediction_Raw_files_validated/Bad_Raw/'

            if os.path.isdir(source):

                path = "PredictionArchiveBadData"

                if not os.path.isdir(path):

                    os.makedirs(path)

                dest = 'PredictionArchiveBadData/BadData_' + str(date)+"_"+str(time)
                if not os.path.isdir(dest):
                    os.makedirs(dest)

                files = os.listdir(source)
                for f in files:
                    if f not in os.listdir(dest):
                        shutil.move(source + f, dest)

                self.logger.info("Bad files moved to archive")
                path = 'Prediction_Raw_files_validated/'

                if os.path.isdir(path + 'Bad_Raw/'):
                    shutil.rmtree(path + 'Bad_Raw/')
                self.logger.info("Bad Raw Data Folder Deleted successfully!!")

        except Exception as e:
            self.logger.info( "Error while moving bad files to archive:: %s" % e)
            raise e



    def validationFileNameRaw(self,regex,LengthOfDateStampInFile,LengthOfTimeStampInFile):

        self.DeletingDirectoryForBadRawData()
        self.DeletingDirectoryForGoodRawData()
        self.creatingDirectoryForGoodBadRawData()
        onlyfiles = [f for f in listdir(self.Batch_Directory)]

        try:
            for filename in onlyfiles:
                if (re.match(regex, filename)):
                    splitAtDot = re.split('.csv', filename)
                    splitAtDot = (re.split('_', splitAtDot[0]))
                    if len(splitAtDot[1]) == LengthOfDateStampInFile:
                        if len(splitAtDot[2]) == LengthOfTimeStampInFile:
                            shutil.copy("Prediction_File/" + filename, "Prediction_Raw_files_validated/Good_Raw")
                            self.logger.info("Valid File name!! File moved to GoodRaw Folder :: %s" % filename)

                        else:
                            shutil.copy("Prediction_File/" + filename, "Prediction_Raw_files_validated/Bad_Raw")
                            self.logger.info("Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)
                    else:
                        shutil.copy("Prediction_File/" + filename, "Prediction_Raw_files_validated/Bad_Raw")
                        self.logger.info("Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)
                else:
                    shutil.copy("Prediction_File/" + filename, "Prediction_Raw_Files_Validated/Bad_Raw")
                    self.logger.info("Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)

            
        except Exception as e:
            self.logger.info("Error occured while validating FileName %s" % e)
            raise e

    def validatingColumnLength(self,NumberOfColumn):

        """Validating column number in csv """


        self.logger.info('{} CHECKING NUMBER OF COLUMN {}'.format('='*20,'='*20))


        try:

            for i in listdir('Prediction_Raw_files_validated/Good_Raw/'):

                file = pd.read_csv('Prediction_Raw_files_validated/Good_Raw/' + i)

                if file.shape[1] != NumberOfColumn:

                     shutil.move("Prediction_Raw_files_validated/Good_Raw/" + file, "Prediction_Raw_files_validated/Bad_Raw")

                     self.logger.info('Bad file moved to bad directory not having validated column number file name is : {}'.format(i))

                else:
                    pass

            self.logger.info('Succesfully ended file column checking')

        except OSError as s:

            self.logger.info('OsError occured while validating column name is : ' + str(s))

        except Exception as e:

            self.logger.info('Exception Error occured while validating column name is : ' + str(e))

       

    def validateMissingValuesInWholeColumn(self):
        """ validate whole missing value column
                              """
        try:
            
            self.logger.info("{} Missing Values Validation Started!! {}".format('='*20,'='*20))

            for file in listdir('Prediction_Raw_files_validated/Good_Raw/'):
                csv = pd.read_csv("Prediction_Raw_files_validated/Good_Raw/" + file)
                count = 0
                for columns in csv:
                    if (len(csv[columns]) - csv[columns].count()) == len(csv[columns]):
                        count+=1
                        shutil.move("Prediction_Raw_files_validated/Good_Raw/" + file,
                                    "Prediction_Raw_files_validated/Bad_Raw")
                        self.logger.info("Invalid Column Length for the file!! File moved to Bad Raw Folder :: %s" % file)
                        break
                if count==0:
                    csv.to_csv("Prediction_Raw_files_validated/Good_Raw/" + file, index=None, header=True)
            self.logger.info('Successfully ended missing WholeColumn check')
        except OSError:
            self.logger.info("Error Occured while moving the file :: %s" % OSError)
            raise OSError
        except Exception as e:
            self.logger.info( "Error Occured:: %s" % e)
            raise e
    def deletePredictionFile(self):

        if os.path.exists('Prediction_Output_File/Predictions.csv'):
            os.remove('Prediction_Output_File/Predictions.csv')
