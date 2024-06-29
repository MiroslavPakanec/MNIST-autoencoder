import uuid
import traceback
import numpy as np
from loguru import logger
from fastapi import APIRouter, Response, Body
from starlette.responses import JSONResponse

import src.visualizer as visualizer
from src.dtos.sample_dto import MNISTSample
import src.loaders.data_db_loader as db_loader

sampling_router = APIRouter()

@sampling_router.get('/train_sample_image')
def train_sample_image():
    try:
        sample_x, sample_y = db_loader.load_train_sample()
        image: bytes = visualizer.get_samples_image(sample_x, sample_y)
        image_filename = f'train_sample_{uuid.uuid4()}.png'
        image_headers = {'Content-Disposition': 'inline; filename=image_filename'}
        return Response(image, headers=image_headers, media_type='image/png')
    except Exception as e:
        logger.error('[GENERIC ERROR]')
        logger.error(traceback.format_exc())
        return JSONResponse(content={'error': 'Server failed to process request'}, status_code=500)

@sampling_router.get('/train_sample')
def train_sample():
    try:
        np_sample_x, np_sample_y = db_loader.load_train_sample()
        sample_x, sample_y = np_sample_x.tolist(), np_sample_y.tolist()
        return { 'x': sample_x, 'y': sample_y }
    except Exception as e:
        logger.error('[GENERIC ERROR]')
        logger.error(traceback.format_exc())
        return JSONResponse(content={'error': 'Server failed to process request'}, status_code=500)

@sampling_router.get('/test_sample_image')
def test_sample_image():
    try:
        sample_x, sample_y = db_loader.load_test_sample()
        image: bytes = visualizer.get_samples_image(sample_x, sample_y)
        image_filename = f'test_sample_{uuid.uuid4()}.png'
        image_headers = {'Content-Disposition': 'inline; filename=image_filename'}
        return Response(image, headers=image_headers, media_type='image/png')
    except Exception as e:
        logger.error('[GENERIC ERROR]')
        logger.error(traceback.format_exc())
        return JSONResponse(content={'error': 'Server failed to process request'}, status_code=500)
    
@sampling_router.get('/test_sample')
def test_sample():
    try:
        np_sample_x, np_sample_y = db_loader.load_test_sample()
        sample_x, sample_y = np_sample_x.tolist(), np_sample_y.tolist()
        return { 'x': sample_x, 'y': sample_y }
    except Exception as e:
        logger.error('[GENERIC ERROR]')
        logger.error(traceback.format_exc())
        return JSONResponse(content={'error': 'Server failed to process request'}, status_code=500)
    
@sampling_router.post('/sample_to_image')
def sample_to_image(sample: MNISTSample = Body(..., example=[0]*784)):
    try:
        np_sample = np.array(sample)
        image: bytes = visualizer.get_sample_image(np_sample)
        image_filename = f'sample_{uuid.uuid4()}.png'
        image_headers = {'Content-Disposition': 'inline; filename=image_filename'}
        return Response(image, headers=image_headers, media_type='image/png')
    except Exception as e:
        logger.error('[GENERIC ERROR]')
        logger.error(traceback.format_exc())
        return JSONResponse(content={'error': 'Server failed to process request'}, status_code=500)