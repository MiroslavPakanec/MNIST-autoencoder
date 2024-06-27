from typing import List, Literal, Union
from pydantic import BaseModel


class EncoderLayerConfig(BaseModel):
    in_channels: int
    out_channels: int
    kernel_size: int
    stride: int
    padding: int
    activation: Union[Literal['relu'], Literal['sigmoid']]

class DecoderLayerConfig(BaseModel):
    in_channels: int
    out_channels: int
    kernel_size: int
    stride: int
    padding: int
    output_padding: int
    activation: Union[Literal['relu'], Literal['sigmoid']]

class ModelConfig(BaseModel):
    encoder_layers: List[EncoderLayerConfig]
    decoder_layers: List[DecoderLayerConfig]