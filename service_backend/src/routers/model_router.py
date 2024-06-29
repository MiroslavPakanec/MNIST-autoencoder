import uuid
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