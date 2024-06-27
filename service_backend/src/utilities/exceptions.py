import traceback
from loguru import logger
from fastapi import HTTPException

class WatermarkConfigException(Exception):
    def __init__(self):
        super().__init__('Failed to load watermark config.')

class WatermarkInputException(Exception):
    def __init__(self, shape) -> None:
        super().__init__(detail=f'Watermark input images have invalid shape {shape}. Expected (n, 784).')

class ModelConfigException(HTTPException):
    def __init__(self, detail):
        self.log_error(detail)
        super().__init__(status_code=400, detail=detail)
    
    @staticmethod
    def log_error(detail: str):
        logger.error('[MODEL CONFIG ERROR]')
        logger.error(detail)
        logger.error(traceback.format_exc())