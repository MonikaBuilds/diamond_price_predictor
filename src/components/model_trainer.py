import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from src.exception import CustomException
from src.logger import logging

from src.utils import save_object
from src.utils import evaluate_model

from dataclasses import dataclass
import sys
import os


# Configuration class to store model path
@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts', 'model.pkl')


class ModelTrainer:
    def __init__(self):
        # Initialize model trainer configuration
        self.model_trainer_config = ModelTrainerConfig()
        
    def initiate_model_training(self, train_array, test_array):
        
        try:
            # Logging start of model training
            logging.info(
                'Splitting Dependent and Independent varibales from train and test data'
            )

            # Split input features and target variable
            x_train, y_train, x_test, y_test = (
                train_array[:, :-1],  # all columns except last → features
                train_array[:, -1],   # last column → target
                test_array[:, :-1],
                test_array[:, -1]
            )

            # Dictionary of models to train and evaluate
            models = {
                'linearRegression': LinearRegression(),
                'Lasso': Lasso(),
                'Ridge': Ridge(),
                'ElasticNet': ElasticNet()
            }

            # Evaluate all models and get performance report
            model_report: dict = evaluate_model(
                x_train, y_train, x_test, y_test, models
            )

            # Print model performance scores
            print(model_report)
            print('\n=====================================================================')
            logging.info(f'Model Report : {model_report}')
                
            # Get best model score from evaluation report
            best_model_score = max(sorted(model_report.values()))
                
            # Get the name of the best performing model
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            # Fetch the best model object
            best_model = models[best_model_name]
            
            # Print and log best model details
            print(
                f'Best model Found, Model Name: {best_model_name}, R2 Score: {best_model_score}'
            )
            print('\n=====================================================================')
            logging.info(
                f'Best Model Found , Model Name : {best_model_name} , R2 Score : {best_model_score}'
            )
                
            # Save the trained best model to disk
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

        except Exception as e:
            # Log exception if any error occurs during training
            logging.info('Exception occured at Model Training')
            raise CustomException(e, sys)
