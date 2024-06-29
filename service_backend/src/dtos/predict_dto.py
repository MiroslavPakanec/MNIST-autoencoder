from pydantic import BaseModel
from src.dtos.model_dto import ModelConfig
from src.dtos.sample_dto import MNISTSample


class Predict(BaseModel):
    experiment_id: str
    sample: MNISTSample