import os
import sys
import pickle
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

from src.exception import CustomException
from src.logger import logging


#  SAVE MODEL 
def save_model(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

        logging.info("Model saved successfully")

    except Exception as e:
        raise CustomException(e, sys)


# LOAD MODEL
def load_model(file_path):   
    try:
        with open(file_path, 'rb') as file_obj:
            logging.info("Model loaded successfully")
            return pickle.load(file_obj)

    except Exception as e:
        logging.info('Exception occurred in load_model function utils')
        raise CustomException(e, sys)


#  EVALUATE MODEL
def evaluate_model(x_train, y_train, x_test, y_test, models):
    try:
        report = {}

        for model_name, model in models.items():

            # Train model
            model.fit(x_train, y_train)

            # Predict train & test data
            y_train_pred = model.predict(x_train)
            y_test_pred = model.predict(x_test)

            # R2 Scores
            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            # Save test score
            report[model_name] = test_model_score

            logging.info(
                f"{model_name} --> Train R2: {train_model_score}, Test R2: {test_model_score}"
            )

        return report

    except Exception as e:
        raise CustomException(e, sys)
