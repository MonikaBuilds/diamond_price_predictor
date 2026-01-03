import sys
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.preprocessing import OneHotEncoder

from src.exception import CustomException
from src.logger import logging
from src.utils import save_model

@dataclass
class DataTransformationConfig:
    preprosessor_obj_file:str = os.path.join("artifacts","preprocessing.pkl")
    
class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
    
    def get_data_transformation_object(self):
        try:
            logging.info('Data Transformation initiated')
        
            # Define which column should be ordinal-encoded and which should be scaled
            numerical_column = ['carat', 'depth', 'table', 'x', 'y', 'z']
            categorical_column = ['cut', 'color', 'clarity']

        
        
            logging.info('Pipeline initiated')
        
            # Numerical Pipeline
            num_Pipeline = Pipeline([
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler())
            ])
        
            # Categorical Pipeline
            cat_Pipeline = Pipeline([
                ('imputer', SimpleImputer(strategy="most_frequent")),
                ('encoder',OneHotEncoder(handle_unknown='ignore')),

            ])
        
            # Combine into ColumnTransformer
            preprocessor = ColumnTransformer([
                ('num_Pipeline', num_Pipeline, numerical_column),
                ('categorical_Pipeline', cat_Pipeline, categorical_column)
            ])

            logging.info('Pipeline completed')
            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)
    
    def initiate_data_transformation(self, train_path, test_path):
        try:
            # Reading train and test data
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            
        
            logging.info('Read train and test data completed')
            logging.info(f"Train DataFrame Head : \n{train_df.head().to_string()}")
            logging.info(f"Test DataFrame Head : \n{test_df.head().to_string()}")

            logging.info('Obtaining preprocessing object')
            preprocessing_obj = self.get_data_transformation_object()
        
            target_column_name = 'price'
            drop_columns = [col for col in ['price', 'id'] if col in train_df.columns]

            input_feature_train_df = train_df.drop(columns=drop_columns, axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=drop_columns, axis=1)
            target_feature_test_df = test_df[target_column_name]
        
            # Transform using processor object
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            logging.info("Applying preprocessing object on training and testing datasets.")
        
            # Combine features and target
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
        
            # Ensure folder exists before saving
            os.makedirs(os.path.dirname(self.data_transformation_config.preprosessor_obj_file), exist_ok=True)

            save_model(
                file_path=self.data_transformation_config.preprosessor_obj_file,
                obj=preprocessing_obj
            )

            logging.info('Preprocessor pickle file saved')
        
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprosessor_obj_file,
            )

        except Exception as e:
            logging.info("Exception occurred in the initiate_data_transformation")
            raise CustomException(e, sys)


if __name__=='__main__':
    obj = DataTransformation()

    train_path = os.path.join("artifacts", "train.csv")
    test_path  = os.path.join("artifacts", "test.csv")

    obj.initiate_data_transformation(train_path, test_path)
