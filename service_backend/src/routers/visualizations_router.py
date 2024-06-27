import uuid
import traceback
from loguru import logger
import src.visualizer as visualizer
from fastapi import APIRouter, Response
from starlette.responses import JSONResponse
import src.loaders.data_db_loader as db_loader

visualizations_router = APIRouter()

@visualizations_router.post('/train_sample')
def train_sample():
    try:
        sample_x, sample_y = db_loader.load_train_sample()
        image: bytes = visualizer.get_sample_image(sample_x, sample_y)
        image_filename = f'train_sample_{uuid.uuid4()}.png'
        image_headers = {'Content-Disposition': 'inline; filename=image_filename'}
        return Response(image, headers=image_headers, media_type='image/png')
    except Exception as e:
        logger.error('[GENERIC ERROR]')
        logger.error(traceback.format_exc())
        return JSONResponse(content={'error': 'Server failed to process request'}, status_code=500)
    
@visualizations_router.post('/test_sample')
def test_sample():
    try:
        sample_x, sample_y = db_loader.load_test_sample()
        image: bytes = visualizer.get_sample_image(sample_x, sample_y)
        image_filename = f'test_sample_{uuid.uuid4()}.png'
        image_headers = {'Content-Disposition': 'inline; filename=image_filename'}
        return Response(image, headers=image_headers, media_type='image/png')
    except Exception as e:
        logger.error('[GENERIC ERROR]')
        logger.error(traceback.format_exc())
        return JSONResponse(content={'error': 'Server failed to process request'}, status_code=500)