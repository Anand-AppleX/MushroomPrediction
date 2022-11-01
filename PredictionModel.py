from logger import logging
from data_ingestion import data_loader_pred
import pandas as pd
from data_preprocessing import preprosessing
import pickle
import os
from PredictionDataValidation.PredictionValidation import  Prediction_Data_validation
from File_Operation import fileMethod
class prediction:

    def __init__(self,path):

        self.logger = logging
        self.pred_data_val = Prediction_Data_validation(path)

    def PredModel(self):

        self.pred_data_val.deletePredictionFile()

        try:

            self.logger.info('{} Pred Model Preprocessing Started {}'.format('='*20,'='*20))

            data = data_loader_pred.Data_getter().load_data()

            preprocessors = preprosessing.preprocessor()

            data = preprocessors.removecolumn(data,'veil_type')

            null_present = preprocessors.is_null_present(data)

            if (null_present):
                data = preprocessors.impute_missing_value(data)

            ohe = pickle.load(open(r'C:\Users\vijit\Mashroom\pickle_folder\ohetest.pkl','rb'))

            data = ohe.transform(data)

            data = pd.DataFrame(data)

            self.logger.info('{} Prediction Model Preprocessing Ended {}'.format('='*20,'='*20))

            self.logger.info('{} Prediction Model Clustering Started {}'.format('='*20,'='*20))

            kmean = pickle.load(open('C:\\Users\\vijit\\Mashroom\\pickle_folder\\KMean.pkl','rb'))

            clusters=kmean.predict(data)

            data['clusters']=clusters

            clusters=data['clusters'].unique()

            self.logger.info('{} Prediction Model Clustering Ended {}'.format('='*20,'='*20))

            result=[]
            file_loader=fileMethod.File_Operation()

            for i in clusters:
                cluster_data= data[data['clusters']==i]
                cluster_data = cluster_data.drop(['clusters'],axis=1)
                model_name = file_loader.find_correct_model_file(i)
                model = file_loader.load_model(model_name)
                for val in (model.predict(cluster_data)):
                    result.append(val)

            d = {1:'p',0:'e'}

            result = result

            path = "Prediction_Output_File/"

            if not os.path.isdir(path):
                os.makedirs(path)

            data = data_loader_pred.Data_getter().load_data()

            data['Output'] = result

            data['Output'] = data['Output'].map(d)

            data.to_csv(path + 'Prediction.csv',index=False)

            self.logger.info('{} Prediction File Created {}'.format('='*20,'='*20))

        except Exception as e:

            self.logger.info('Error while prediction is :' + str(e))

            raise e

#prediction(r"C:\Users\vijit\Mashroom\Prediction_File").PredModel()



