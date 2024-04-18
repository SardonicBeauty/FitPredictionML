import sys
from dataclasses import dataclass

import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
import os
from src.utils import save_function

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformation_object(self):
        try:
            logging.info('Data Transformation initiated')
            # Define which columns should be onehot-encoded and which should be scaled
            categorical_cols = ['body_type', 'category']
            numerical_cols = ['weight', 'size', 'age', 'height']
            
            # Define the custom ranking for each ordinal variable
            category_categories = ['pant', 't-shirt', 'jogger', 'knit', 'sweatshirt', 'trousers', 'leggings', 'crewneck', 'parka', 'cardigan', 'midi', 'shift', 'sweatershirt', 
                                   'tight', 'hoodie', 'jumpsuit', 'shirtdress', 'culotte', 'tee', 'for', 'mini', 'turtleneck', 'suit', 'jeans', 'sheath', 'print', 'tunic', 'jacket', 
                                   'sweater', 'kaftan', 'blazer', 'henley', 'blouse', 'overalls', 'trouser', 'culottes', 'romper', 'caftan', 'coat', 'skirts', 'trench', 'cape', 'bomber',
                                   'down', 'ballgown', 'peacoat', 'shirt', 'pullover', 'blouson', 'frock', 'buttondown', 'duster', 'maxi', 'gown', 'legging', 'skort', 'combo', 'tank', 
                                   'kimono', 'cami', 'top', 'dress', 'skirt', 'poncho', 'pants', 'vest', 'overcoat', 'sweatpants']
            body_categories = ["hourglass", "athletic", "petite", "pear", "straight", "full bust", "apple"]
            
            logging.info('Pipeline Initiated')
            ## Numerical Pipeline
            num_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler())
                ]
            )

            # Categorical Pipeline
            cat_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('onehotencoder', OneHotEncoder(categories=[body_categories, category_categories])),
                    ('scaler', StandardScaler(with_mean=False))  # Set with_mean=False
                ]
            )

            preprocessor = ColumnTransformer([
                ('num_pipeline', num_pipeline, numerical_cols),
                ('cat_pipeline', cat_pipeline, categorical_cols)
            ])
            
            logging.info('Pipeline Completed')
            return preprocessor

        except Exception as e:
            logging.info("Error in Data Transformation")
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self, train_path, test_path):
        try:
            # Reading train and test data
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info('Read train and test data completed')
            logging.info(f'Train Dataframe Head : \n{train_df.head().to_string()}')
            logging.info(f'Test Dataframe Head  : \n{test_df.head().to_string()}')

            logging.info('Obtaining preprocessing object')

            preprocessing_obj = self.get_data_transformation_object()

            target_column_name = 'fit_i'
            drop_columns = [target_column_name, 'bust_size']

            input_feature_train_df = train_df.drop(columns=drop_columns, axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=drop_columns, axis=1)
            target_feature_test_df = test_df[target_column_name]
            
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.concatenate((input_feature_train_arr.toarray(), target_feature_train_df.values.reshape(-1, 1)), axis=1)
            test_arr = np.concatenate((input_feature_test_arr.toarray(), target_feature_test_df.values.reshape(-1, 1)), axis=1)

            save_function(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            logging.info('Preprocessor pickle file saved')

            return train_arr, test_arr, self.data_transformation_config.preprocessor_obj_file_path
            
        except Exception as e:
            logging.info("Exception occurred in the initiate_data_transformation")
            raise CustomException(e, sys)
