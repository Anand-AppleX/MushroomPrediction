import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kneed import KneeLocator
from logger import logging
import pickle

class Kmeans:

    def __init__(self):

        self.logger = logging

    def elbow_method(self,data):
        
        self.logger.info('{} USING EBLOW METHOD {} '.format('='*20,'='*20))

        self.data = data
        wcss = []
        try:

            
            for i in range(1,11):
                kmeans = KMeans(n_clusters=i,init='k-means++',random_state=42)
                kmeans.fit(self.data)
                wcss.append(kmeans.inertia_)
            plt.plot(range(1,11),wcss)

            plt.xlabel('cluster')
            plt.ylabel(wcss)
            plt.savefig('preprocessing_data/k_mean-Elbow.png')

            self.kn = KneeLocator(range(1, 11), wcss, curve='convex', direction='decreasing')

            self.logger.info('Elbow created successfully and img is saved and number of cluster is {}'.format(self.kn.knee))


            return self.kn.knee

        except Exception as e:

            self.logger.info('Error during elbow plot creation is : ' + str(e))

    def create_cluster(self,data,number_OfCluster):

        """this will create n number of cluster"""

        self.logger.info('{} Creating {} number of cluster'.format('='*20,number_OfCluster,'='*20))
        self.data=data

        try:
            self.kmeans = KMeans(n_clusters=number_OfCluster, init='k-means++', random_state=42)

            self.y_kmeans=self.kmeans.fit_predict(data)

            pickle.dump(self.kmeans,open('pickle_folder/KMean.pkl','wb'))

            self.data['Cluster']=self.y_kmeans

            self.logger.info('Successfully Created {} cluster!!... '.format(number_OfCluster))

            self.logger.info('Kmean pickle loaded to pickle folder')

            return self.data

        except Exception as e:

            self.logger.info('Error while creating cluster is : ' + str(e))



