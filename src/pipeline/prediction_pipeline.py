import sys 
import os 
from src.exception import CustomException 
from src.logger import logging 
from src.utils import load_obj
import pandas as pd

class PredictPipeline: 
    def __init__(self) -> None:
        pass

    def predict(self, features): 
        try: 
            preprocessor_path = os.path.join('artifacts', 'preprocessor.pkl')
            model_path = os.path.join("artifacts", "model.pkl")

            preprocessor = load_obj(preprocessor_path)
            model = load_obj(model_path)

            data_scaled = preprocessor.transform(features)
            pred = model.predict(data_scaled)
            return pred
        except Exception as e: 
            logging.info("Error occured in predict function in prediction_pipeline location")
            raise CustomException(e,sys)
        
class CustomData: 
        def __init__(self, weight:int, 
                     body_type:str, 
                     height:float, 
                     size:int, 
                     age:int, 
                     category:str,  
                    ): 
             self.weight = weight
             self.body_type = body_type
             self.height = height
             self.size = size
             self.age = age
             self.category = category
        def get_data_as_dataframe(self): 
             try: 
                  custom_data_input_dict = {
                       'weight': [self.weight], 
                       'body_type': [self.body_type], 
                       'height': [self.height], 
                       'size': [self.size],
                       'age':[self.age],
                       'category':[self.category], 

                  }
                  df = pd.DataFrame(custom_data_input_dict)
                  logging.info("Dataframe created")
                  return df
             except Exception as e:
                  logging.info("Error occured in get_data_as_dataframe function in prediction_pipeline")
                  raise CustomException(e,sys) 
             