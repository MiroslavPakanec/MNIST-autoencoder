import torch
import mlflow
import functools
import numpy as np
from src.utilities.environment import Environment

def mlflow_tracking(func):
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        experiment_id = args[0] if args else kwargs.get('experiment_id')
        config = args[1] if args else kwargs.get('config')
        if not config:
            raise ValueError("Config parameter is required for MLFlow tracking.")
        
        mlflow.set_tracking_uri(Environment().MLFLOW_TRACKING_URI)
        with mlflow.start_run(run_name=experiment_id):
            mlflow.log_params(config.dict())
            model, train_losses, val_losses = func(*args, **kwargs)           
            mlflow.pytorch.log_model(model, artifact_path='model', registered_model_name=f'{experiment_id}')
            
            mlflow.log_artifact('./.env')
            mlflow.log_artifact('./requirements.api.txt')
            mlflow.log_artifact('./docker-compose.yaml')
            mlflow.log_artifact('./Dockerfile.api')
        return model, train_losses, val_losses
    return wrapper
