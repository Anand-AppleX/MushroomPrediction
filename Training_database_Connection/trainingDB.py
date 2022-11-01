import os
from os import  listdir
from logger import  logging
import pandas as pd
import database_connect as connection
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider


class DBOperation:
    
    def __init__(self):

        self.badFilePath = "Training_Raw_files_validated/Bad_Raw"
        self.goodFilePath = "Training_Raw_files_validated/Good_Raw/"
        self.logger = logging


    def loadtodatabase(self):

        self.logger.info("{} MAKING CONNECTION TO DATABASE {}".format('='*20,'='*20))
        try:

            zip_path = r'D:\secure-connect-mushrooms.zip'
            client_id = 'EzpULDJATbLceuMjSlSSxiqX'
            client_secret = '+d,t_zCvkyGFD2qcST,fwPq,eItIIIjeCkZbdJ8Bj,U9OUgOoX.yAMiyRbZSR,ZwtBTFF3__ST9TFzH813cwM,ZFoB+,HWBO0r6AYwF3fTZ0+q6GuHU,1SZhM0HnHEhZ'
            keyspace = 'mush'
            table_name = 'mushrooms'

            cassandra = connection.cassandra_operations(zip_path,
                                                client_id,
                                                client_secret,
                                                keyspace,
                                            table_name)

            self.logger.info('{} CONNECTION DONE SUCCESSFULLY {}'.format('='*20,'='*20))

            self.logger.info('{} NOW INSERTING DATA INTO TABLE {}'.format('='*20,'='*20))

            cloud_config= {'secure_connect_bundle': 'E:\secure-connect-mushrooms.zip'}
            auth_provider = PlainTextAuthProvider('caOGgwstrqfMbPBIEjpSYBmn','2wPdzqu,wUISxwUmqYXgspRDm..8j-lQL1eZLjCpnsbpZdm9zTKkmMo5i4r8fQeUJ4YHI_+Hzzs.j0DbCe+.gWEPZuqA-M+Z4BcTr7NP9Q_7ZTekpCSZ2-jUxB.2lhC_')
            cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
            session = cluster.connect()
            row = session.execute("select release_version from system.local").one()
            row=session.execute("select * from system_schema.keyspaces")

            session = cluster.connect('mush')

            

            session.execute('DROP TABLE IF EXISTS mush.mushrooms_train;')
            self.logger.info('table dropped!!....')

            for i in os.listdir(self.goodFilePath):

                df = pd.read_csv(self.goodFilePath + i)

                self.logger.info('Reading csv file from good folder done')

                df.columns = ['class','cap-shape', 'cap-surface', 'cap-color', 'bruises', 'odor',
       'gill-attachment', 'gill-spacing', 'gill-size', 'gill-color',
       'stalk-shape', 'stalk-root', 'stalk-surface-above-ring',
       'stalk-surface-below-ring', 'stalk-color-above-ring',
       'stalk-color-below-ring', 'veil-type', 'veil-color', 'ring-number',
       'ring-type', 'spore-print-color', 'population', 'habitat']

                l = list(df.columns)

                l1 = []
                for i in l:
                    if i == 'class':
                        l1.append('Output')
                    elif '-' in i:
                        l1.append(i.replace('-','_'))
                    else:
                        l1.append(i)

                df.columns = l1


                id = []
                for i in range(len(df)):
                    id.append(i)

                df['id'] = id

                self.logger.info('id inserted into data')

                df = df[['id','Output', 'cap_shape', 'cap_surface', 'cap_color', 'bruises', 'odor',
                'gill_attachment', 'gill_spacing', 'gill_size', 'gill_color',
                'stalk_shape', 'stalk_root', 'stalk_surface_above_ring',
                'stalk_surface_below_ring', 'stalk_color_above_ring',
                'stalk_color_below_ring', 'veil_type', 'veil_color', 'ring_number',
                'ring_type', 'spore_print_color', 'population', 'habitat']]

                

                cassandra.bulk_upload(data = df,table_name='mushrooms_train',create_new_table=True)

                self.logger.info('Table created successfully and insertion done to database')



        except OSError as s:

            self.logger.info('OSError occured in database is : ' + str(s))

        except Exception as e:

            self.logger.info('Error occured while creating database is : ' + str(e))


    def selectingfromdatabase(self):

        try:

            zip_path = r'D:\secure-connect-mushrooms.zip'
            client_id = 'EzpULDJATbLceuMjSlSSxiqX'
            client_secret = '+d,t_zCvkyGFD2qcST,fwPq,eItIIIjeCkZbdJ8Bj,U9OUgOoX.yAMiyRbZSR,ZwtBTFF3__ST9TFzH813cwM,ZFoB+,HWBO0r6AYwF3fTZ0+q6GuHU,1SZhM0HnHEhZ'
            keyspace = 'mush'
            table_name = 'mushrooms'

            cassandra = connection.cassandra_operations(zip_path,
                                                client_id,
                                                client_secret,
                                                keyspace,
                                            table_name)

            #cassandra.session.default_timeout = 30


            self.df = cassandra.read_data(table_name = 'mushrooms_train')

            self.df.drop('id',axis=1,inplace=True)

            path = 'Training_database/'

            if not os.path.isdir(path):
                os.makedirs(path)

            self.df.to_csv('Training_database/InputFile.csv',index=False)

            self.logger.info('Input file created')

        except Exception as e:

            self.logger.info('Error occured during creating input csv file is : ' + str(e))



        
















