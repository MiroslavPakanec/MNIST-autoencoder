import traceback
from loguru import logger
from fastapi import APIRouter
from starlette.responses import JSONResponse

import src.watermark.watermark_controller as watermark_controller
from src.watermark.watermark_controller import WatermarkShapes

watermark_router = APIRouter()

@watermark_router.get('/watermarks')
def get_watermarks():
    try:
        shapes: WatermarkShapes = watermark_controller.get_watermarks()
        return shapes
    except Exception as e:
        logger.error('[GENERIC ERROR]')
        logger.error(traceback.format_exc())
        return JSONResponse(content={'error': 'Server failed to process request'}, status_code=500)