from sklearn.impute import  SimpleImputer
import os
from logger import logging
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import pickle

class preprocessor:

    def __init__(self):

        self.logger = logging

    
    def removecolumn(self,data,column_name):

        self.data = data
        self.columns=column_name

        try:

            self.logger.info('{} REMOVING COLUMN {}')

            self.new_data = self.data.drop(labels=self.columns,axis=1)

            self.logger.info('{} COLUMNS DROPPED SUCCESSFULLY {}'.format('='*20,'='*20))

            return self.new_data

        except Exception as e:

            self.logger.info('Error occurred during dropping column is : ' + str(e))


    def seprate_lable_feature(self,data,label_column_name):

        """This class will seprate data into dependent and independent variable"""

        self.logger.info('{} We are seprating data into dependent and independent columns {}'.format('='*20,'='*20))
        self.data = data
        self.label_column_name = label_column_name
        try:
            self.X = self.data.drop(labels = self.label_column_name,axis=1)
            self.Y = self.data[self.label_column_name]
            self.logger.info('{} We successfully seprate columns into dependent and independent columns!!... {}'.format('='*20,'='*20))
            return self.X,self.Y

        except Exception as e:

            self.logger.info('There is some error while seprating')
            self.logger.info('The error while seprating is : ' + str(e))

            


    def is_null_present(self,data):

        """This method check null value and if exsist it return True else false"""

        self.logger.info('{} No we going to check is null present or not {}'.format('='*20,'='*20))

        self.data = data
        self.null_present = False
        try:
            self.null_counts = self.data.isna().sum()
            for i in self.null_counts:
                if i >= 1:
                    self.null_present = True
                    break
            if(self.null_present):
                dataframe_with_null = pd.DataFrame() # write the logs to see which columns have null values
                dataframe_with_null['columns'] = data.columns
                dataframe_with_null['missing values count'] = np.asarray(data.isna().sum())
                path = 'preprocessing_data/'
                if not os.path.isdir(path):
                    os.makedirs(path)
                
                dataframe_with_null.to_csv('preprocessing_data/null_values.csv')#storing null count into file

                self.logger.info('{} Null csv created {}'.format('='*20,'='*20))

            return self.null_present

        except Exception as e:

            self.logger.info('Error while checking null value is : ' + str(e))


    def impute_missing_value(self,data):

        """This will fill null value with any valuable value"""

        self.logger.info('Now we filling nan with any valuable value using Simple Imputer')
        self.data = data
        
        try:

            imputer = SimpleImputer(strategy='most_frequent',missing_values=np.nan)
            self.new_array = imputer.fit_transform(self.data)
            self.new_data = pd.DataFrame(self.new_array,columns=self.data.columns)
            self.logger.info('Nan value handel successfully!!...')
            return self.new_data

        except Exception as e:

            self.logger.info('There is some error while imputing nan value by valuable value!!...')
            self.logger.info('Error while imputing nan is : '+str(e))
            


    def conversion(self, data):

            self.logger.info( 'Concerting e to 0 and p to 1')
            self.data = data
            try:

                self.data['output'] = self.data['output'].map({'e':0, 'p': 1})

                self.logger.info('mapping done successfully!!...')

                return self.data

            except Exception as e:

                self.logger.info('Error while mapping is : ' + str(e))

                

    def Encoding(self,X):


        self.logger.info('{} NOW encoding DATA {}'.format('='*20,'='*20))

        try:

            ohe = OneHotEncoder(sparse=False,dtype=np.int32,handle_unknown='ignore')

            self.data = ohe.fit_transform(X)

            if not os.path.isdir('pickle_folder/'):
                os.makedirs('pickle_folder/')

            

            pickle.dump(ohe,open('pickle_folder/ohetest.pkl','wb'))

            self.logger.info('One hot encoding done and pickle file crested')

            return self.data


        except Exception as e:

            self.logger.info('Error during encoding is : ' + str(e))



        



    


    

    
    
