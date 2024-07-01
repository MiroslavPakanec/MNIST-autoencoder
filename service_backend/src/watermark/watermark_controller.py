import yaml
import random
import numpy as np
from typing import List, Tuple
from loguru import logger
from dataclasses import dataclass
from src.utilities.exceptions import WatermarkConfigException, WatermarkInputException
from src.utilities.environment import Environment

WatermarkShape = Tuple[int, int]
WatermarkShapes = List[WatermarkShape]

@dataclass
class WatermarkConfig:
    shapes: WatermarkShapes
    min_watermarks: int
    max_watermarks: int
    watermark_value: int

def add_watermarks(images: np.ndarray): 
    config: WatermarkConfig = _load_config()

    if images.shape[1] != 784 and len(images.shape) != 2:
        raise WatermarkInputException(images.shape)

    images_with_watermark = np.copy(images)
    images_with_watermark = images_with_watermark.reshape(-1, 28, 28)
    num_images = len(images_with_watermark)

    mask = np.zeros((num_images, 28, 28), dtype=bool)
    for i in range(num_images):
        num_masks = random.randint(config.min_watermarks, config.max_watermarks)
        for _ in range(num_masks):
            shape = random.choice(config.shapes)
            watermark_w = shape[0]
            watermark_h = shape[1]
            watermark_x = random.randint(0, 28)
            watermark_y = random.randint(0, 28)
            mask[i, watermark_x:watermark_x + watermark_w, watermark_y:watermark_y + watermark_h] = True
    images_with_watermark[mask] = config.watermark_value
    images_with_watermark = images_with_watermark.reshape(-1, 784)
    return images_with_watermark  

def get_watermarks() -> WatermarkShapes:
    config: WatermarkConfig = _load_config()
    shapes: WatermarkShapes = config.shapes
    return shapes


def _load_config() -> WatermarkConfig:
    try:
        with open(Environment().WATERMARK_CONFIG_PATH, 'r') as file:
            data = yaml.safe_load(file)
            return WatermarkConfig(
                shapes=data['shapes'],
                min_watermarks=data['min_number_of_watermarks_per_image'],
                max_watermarks=data['max_number_of_watermarks_per_image'],
                watermark_value= data['watermark_value']
            )
    except Exception as e:
        logger.debug(e)
        raise WatermarkConfigException()