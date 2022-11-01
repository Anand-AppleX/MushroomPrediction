from logger import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score,roc_auc_score
from sklearn.neighbors import KNeighborsClassifier

class model_finder:

    def __init__(self):

        self.logger = logging
        self.ram = RandomForestClassifier()
        self.knn = KNeighborsClassifier()


    def get_best_param_randomforest(self,X_train,y_train):

        self.logger.info('{} Rsndom Forest {}'.format('='*20,'='*20))

        try:

            self.param_grid = {"n_estimators": [10, 50, 100, 130], "criterion": ['gini', 'entropy'],
                               "max_depth": range(2, 4, 1), "max_features": ['auto', 'log2']}

            self.random = GridSearchCV(estimator=self.ram, param_grid=self.param_grid, cv=5,  verbose=3)

            self.random.fit(X_train,y_train)

            self.criterion = self.random.best_params_['criterion']
            self.n_estimators = self.random.best_params_['n_estimators']
            self.max_depth = self.random.best_params_['max_depth']
            self.max_features = self.random.best_params_['max_features']

            self.ram = RandomForestClassifier(n_estimators=self.n_estimators,criterion=self.criterion,max_depth=self.max_depth,max_features=self.max_features)

            self.ram.fit(X_train,y_train)

            self.logger.info('Random forest best param are :  {}'.format(self.random.best_params_))

            return self.ram

        except Exception as e:

            self.logger.info('Error during random forest is : '+ str(e))



    def get_best_params_for_KNN(self, train_x, train_y):

        self.logger.info('Entered the get_best_params_for_Ensembled_KNN method of the Model_Finder class')
        try:

            self.param_grid_knn = {
                'algorithm' : ['ball_tree', 'kd_tree', 'brute'],
                'leaf_size' : [10,17,24,28,30,35],
                'n_neighbors':[4,5,8,10,11],
                'p':[1,2]
            }


            self.grid = GridSearchCV(self.knn, self.param_grid_knn, verbose=3,
                                     cv=5)

            self.grid.fit(train_x, train_y)

            self.algorithm = self.grid.best_params_['algorithm']
            self.leaf_size = self.grid.best_params_['leaf_size']
            self.n_neighbors = self.grid.best_params_['n_neighbors']
            self.p  = self.grid.best_params_['p']

            self.knn = KNeighborsClassifier(algorithm=self.algorithm, leaf_size=self.leaf_size, n_neighbors=self.n_neighbors,p=self.p,n_jobs=-1)

            self.knn.fit(train_x, train_y)
            self.logger.info( 'KNN best params: ' + str(self.grid.best_params_) + '. Exited the KNN method of the Model_Finder class')
            return self.knn
        except Exception as e:

            self.logger.info('Error while Kneighbour is : ' + str(e))


    def get_best_model(self,train_x,train_y,test_x,test_y):

        """ This class help to give best model for prediction """
        self.logger.info('{} Entered the get_best_model method of the Model_Finder class {}'.format('='*20,'='*20))

        try:
            

            # create best model for Random Forest
            self.random_forest=self.get_best_param_randomforest(train_x,train_y)
            self.prediction_random_forest=self.random_forest.predict(test_x) # prediction using the Random Forest Algorithm

            if len(test_y.unique()) == 1:#if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
                self.random_forest_score = accuracy_score(test_y,self.prediction_random_forest)
                self.logger.info( 'Accuracy for RF:' + str(self.random_forest_score))
            else:
                self.random_forest_score = roc_auc_score(test_y, self.prediction_random_forest) # AUC for Random Forest
                self.logger.info('AUC for RF:' + str(self.random_forest_score))

            self.knn= self.get_best_params_for_KNN(train_x,train_y)
            self.prediction_knn = self.knn.predict(test_x) # Predictions using the KNN Model

            if len(test_y.unique()) == 1: #if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
                self.knn_score = accuracy_score(test_y, self.prediction_knn)
                self.logger.info('Accuracy for knn:' + str(self.knn_score))  # Log AUC
            else:
                self.knn_score = roc_auc_score(test_y, self.prediction_knn) # AUC for KNN
                self.logger.info('AUC for knn:' + str(self.knn_score)) # Log AUC

            #comparing the two models
            if(self.random_forest_score <  self.knn_score):
                return 'KNN',self.knn

            else:
                return 'RF',self.ram

        except Exception as e:

            self.logger.info('Error during best model selection is : ' + str(e))


        
