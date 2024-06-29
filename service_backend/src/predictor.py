import torch
from typing import List
from loguru import logger
from src.mlflow import load_model
from src.dtos.sample_dto import MNISTSample


def predict(experiment_id: str, sample: MNISTSample) -> List[int]:
    device = get_device()
    model = get_model(experiment_id, device)
    sample_tensor = get_tensor(sample, device)

    with torch.no_grad():
        prediction = model(sample_tensor)
    
    predicted_pixels = prediction.view(-1).mul(255).clamp(0, 255).byte().tolist()
    return predicted_pixels

def get_tensor(sample: MNISTSample, device):
    sample_tensor = torch.tensor(sample, dtype=torch.float32).view(1, 1, 28, 28) / 255.0
    sample_tensor = sample_tensor.to(device)
    return sample_tensor

def get_model(experiment_id: str, device):
    model = load_model(experiment_id).to(device)
    return model

def get_device():
    if torch.cuda.is_available():
        logger.info('[Training on GPU]')
        logger.info(f'[Device: {torch.cuda.get_device_name(0)}]')
        return torch.device('cuda')
    else:
        logger.info('[Training on CPU]')
        return torch.device('cpu')