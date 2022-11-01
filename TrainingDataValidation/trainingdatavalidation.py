import os
from logger import logging
import json
import shutil
import re
from os import listdir
from datetime import datetime
import pandas as pd

class training_validation:

    def __init__(self,path):

        self.Batch_Directory = path
        self.schema = "schema_training.json"
        self.logger = logging

    def valuesfromschema(self):

        """This class will give all values from schema"""

        self.logger.info("======================VALUE FROM SCHEMA PATH======================")
        try:

            with open(self.schema,'r') as f:
                dic = json.load(f)

                f.close()
            Samplefilename = dic['SampleFileName']
            
            
            NumberOfColumns = dic['NumberOfColumns']

            column_name = dic['ColName']


            self.logger.info("SampleFileName is {} number of columns is {}".format(Samplefilename,NumberOfColumns))

            return NumberOfColumns,column_name
        except ValueError:

            self.logger.info('Error occured is : {}'.format(ValueError))

            raise ValueError

        except KeyError:

            self.logger.info('Error occured is : {}'.format(KeyError))
            raise KeyError

        except Exception as e :

            self.logger.info('Error occured is : ' + str(e))

            raise e


    def makingregex(self):

        """In this class we define regex for file name """

        self.logger.info("{}MAKING REGEX{}".format('='*20,'='*20))

        regex = "['mushrooms']+\.csv"

        return regex


    def creatingDirectoryForGoodBadRawData(self):

        """This will create Good and Bad directory """

        try:
            path = os.path.join("Training_Raw_files_validated/", "Good_Raw/")
            if not os.path.isdir(path):
                os.makedirs(path)

            self.logger.info('{} Making Training_Raw_files_validated {}'.format('='*20,'='*20))

            path = os.path.join("Training_Raw_files_validated/", "Bad_Raw/")

            if not os.path.isdir(path):

                os.makedirs(path)
            self.logger.info('{} Making Training_Raw_files_validated done {}'.format('='*20,'='*20))


        except OSError:

            self.logger.info('Error occured is : ' + str(OSError))

            raise OSError


    def DeletingDirectoryForBadRawData(self):

        """ This class will delete bad directory  """
        try:

            path = "Training_Raw_files_validated/"

            if os.path.isdir(path + 'Bad_Raw/'):

                shutil.rmtree(path + 'Bad_Raw/')

                self.logger.info('{} Deleted BAD Directory {}'.format('='*20,'='*20))

        except OSError as s:

            self.logger.info('Error while deleting bad directory is : ' + str(s))

    def DeletingDirectoryForGoodRawData(self):

        """ This class will delete bad directory  """
        try:

            path = "Training_Raw_files_validated/"

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

            source = 'Training_Raw_files_validated/Bad_Raw/'

            if os.path.isdir(source):

                path = "TrainingArchiveBadData"

                if not os.path.isdir(path):

                    os.makedirs(path)

                dest = 'TrainingArchiveBadData/BadData_' + str(date)+"_"+str(time)
                if not os.path.isdir(dest):
                    os.makedirs(dest)

                files = os.listdir(source)
                for f in files:
                    if f not in os.listdir(dest):
                        shutil.move(source + f, dest)

                self.logger.info("Bad files moved to archive")
                path = 'Training_Raw_files_validated/'

                if os.path.isdir(path + 'Bad_Raw/'):
                    shutil.rmtree(path + 'Bad_Raw/')
                self.logger.info("Bad Raw Data Folder Deleted successfully!!")

        except Exception as e:
            self.logger.info( "Error while moving bad files to archive:: %s" % e)
            raise e


    def validatingnameofFile(self,regex):

        
        self.DeletingDirectoryForBadRawData()
        self.DeletingDirectoryForGoodRawData()

        self.creatingDirectoryForGoodBadRawData()

        try :

            self.logger.info('{} Strated file name check {}'.format('='*20,'='*20))

            for files in os.listdir(self.Batch_Directory):

                if (re.match(regex, files)):
                        shutil.copy("Training_Batch_Files/" + files, "Training_Raw_files_validated/Good_Raw")

                        self.logger.info('Validated file by name is send to Good_Raw file name is {}'.format(files))

                else:

                    shutil.copy("Training_Batch_Files/" + files, "Training_Raw_files_validated/Bad_Raw")

                    self.logger.info('Unvalidated file by name is send to Bad_Raw file name is {}'.format(files))
            self.logger.info('Succesfully ended file name checking')

        except Exception as e:

            self.logger.info('Error occured during file name validation is : ' + str(e))

            raise e 





    def validatingColumnLength(self,NumberOfColumn):

        """Validating column number in csv """


        self.logger.info('{} CHECKING NUMBER OF COLUMN {}'.format('='*20,'='*20))


        try:

            for i in listdir('Training_Raw_files_validated/Good_Raw/'):

                file = pd.read_csv('Training_Raw_files_validated/Good_Raw/' + i)

                if file.shape[1] != NumberOfColumn:

                     shutil.move("Training_Raw_files_validated/Good_Raw/" + file, "Training_Raw_files_validated/Bad_Raw")

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

            for file in listdir('Training_Raw_files_validated/Good_Raw/'):
                csv = pd.read_csv("Training_Raw_files_validated/Good_Raw/" + file)
                count = 0
                for columns in csv:
                    if (len(csv[columns]) - csv[columns].count()) == len(csv[columns]):
                        count+=1
                        shutil.move("Training_Raw_files_validated/Good_Raw/" + file,
                                    "Training_Raw_files_validated/Bad_Raw")
                        self.logger.info("Invalid Column Length for the file!! File moved to Bad Raw Folder :: %s" % file)
                        break
                if count==0:
                    csv.to_csv("Training_Raw_files_validated/Good_Raw/" + file, index=None, header=True)
            self.logger.info('Successfully ended missing WholeColumn check')
        except OSError:
            self.logger.info("Error Occured while moving the file :: %s" % OSError)
            raise OSError
        except Exception as e:
            self.logger.info( "Error Occured:: %s" % e)
            raise e
















            

    


            



        






        






        