import traceback
from loguru import logger
import src.trainer as trainer
from fastapi import APIRouter
from starlette.responses import JSONResponse
from src.dtos.train_dto import TrainConfig

model_router = APIRouter()

@model_router.post('/train')
def train(config: TrainConfig):
    try:
        trainer.train(config)
    except Exception as e:
        logger.error('[GENERIC ERROR]')
        logger.error(traceback.format_exc())
        return JSONResponse(content={'error': 'Server failed to process request'}, status_code=500)