class WatermarkConfigException(Exception):
    def __init__(self):
        super().__init__('Failed to load watermark config.')

class WatermarkInputException(Exception):
    def __init__(self, shape) -> None:
        super().__init__(detail=f'Watermark input images have invalid shape {shape}. Expected (n, 784).')