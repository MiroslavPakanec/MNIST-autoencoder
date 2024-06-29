import numpy as np
from typing import List
import uuid
import traceback
from loguru import logger
from src.dtos.predict_dto import Predict
import src.trainer as trainer
from fastapi import APIRouter, Response
from src.predictor import predict
from starlette.responses import JSONResponse
from src.dtos.train_dto import TrainConfig
import src.loaders.data_db_loader as db_loader
import src.visualizer as visualizer

model_router = APIRouter()

@model_router.post('/train')
def train(config: TrainConfig):
    try:
        experiment_id: str = str(uuid.uuid4())
        trainer.train(experiment_id, config)
        return {
            'message': f'Training finished successfully.',
            'experiment_id': experiment_id
        }
    except Exception as e:
        logger.error('[GENERIC ERROR]')
        logger.debug(e)
        logger.error(traceback.format_exc())
        return JSONResponse(content={'error': 'Server failed to process request', 'experiment_id': experiment_id}, status_code=500)
    

@model_router.post('/predict')
def predict_endpoint(request: Predict):
    try:
        predicted_pixels: List[int] = predict(request.experiment_id, request.sample)
        return { 'y': predicted_pixels }
    except Exception as e:
        logger.error('[GENERIC ERROR]')
        logger.debug(e)
        logger.error(traceback.format_exc())
        return JSONResponse(content={'error': 'Server failed to process request'}, status_code=500)
    