from logger import logging
from data_ingestion import data_loader
from sklearn.model_selection import train_test_split
from data_preprocessing import preprosessing
from data_preprocessing import clustering
from best_model import tuner
import pandas as pd
from File_Operation import fileMethod

import pickle


class trainModel:


    def __init__(self) :
        
        self.logger = logging

    def trainingModel(self):
        try:

            self.logger.info('{} Model Preprocessing Started {}'.format('='*20,'='*20))

            data = data_loader.Data_getter().load_data()

            preprocessors = preprosessing.preprocessor()

            data = preprocessors.removecolumn(data,'veil_type')

            data = preprocessors.conversion(data)# e : 0 p: 1

            X,y = preprocessors.seprate_lable_feature(data,label_column_name='output')

            null_present = preprocessors.is_null_present(X)

            if (null_present):
                X = preprocessors.impute_missing_value(X)

            X = preprocessors.Encoding(X)

            self.logger.info('{} Model Preprocessing Ended {}'.format('='*20,'='*20))
            self.logger.info('{} Model Clustering Started {}'.format('='*20,'='*20))

            df = pd.DataFrame(X)

            kn = clustering.Kmeans().elbow_method(X)

            X = clustering.Kmeans().create_cluster(df,kn)

            X['Labels'] = y

            list_of_clusters=X['Cluster'].unique()

            for i in list_of_clusters:
                cluster_data=X[X['Cluster']==i] # filter the data for one cluster

                        # Prepare the feature and Label columns
                cluster_features=cluster_data.drop(['Labels','Cluster'],axis=1)
                cluster_label= cluster_data['Labels']

                        # splitting the data into training and test set for each cluster one by one
                x_train, x_test, y_train, y_test = train_test_split(cluster_features, cluster_label, test_size=0.3, random_state=42)

                model_finder=tuner.model_finder() # object initialization

                        #getting the best model for each of the clusters
                best_model_name,best_model=model_finder.get_best_model(x_train,y_train,x_test,y_test)

                        #saving the best model to the  file directory.

                file_op = fileMethod.File_Operation()
                save_model=file_op.save_model(best_model,best_model_name+str(i))

                    # logging the successful Training
                self.logger.info('{} Successful End of Training {}'.format('='*20,'='*20))

        except Exception as e:

            self.logger.info('Error while training model is : ' + str(e))

