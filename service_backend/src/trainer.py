import torch
import numpy as np
from typing import Tuple
from loguru import logger
from torch import Tensor, nn, optim

from src.model.model import Autoencoder
from src.dtos.train_dto import TrainConfig
import src.loaders.data_db_loader as data_loader


def train(config: TrainConfig):
    device = get_device()
    model = get_model(device, config)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=config.learning_rate)
    xs_train, ys_trian, xs_val, ys_val = get_train_data(device, config)
    
    train_losses = np.zeros(config.epochs)
    val_losses = np.zeros(config.epochs)
    for epoch in range(config.epochs):
        model.train()
        permutation = torch.randperm(xs_train.size(0))
        xs_shuffled = xs_train[permutation]
        ys_shufflex = ys_trian[permutation]
        
        epoch_train_loss = 0.0
        for (xs, ys_true) in get_batches(xs_shuffled, ys_shufflex, config.batch_size):
            ys_pred = model(xs)
            loss = criterion(ys_pred, ys_true)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            epoch_train_loss += loss.item() * xs.size(0)
        train_losses[epoch] = epoch_train_loss / xs_train.size(0)

        model.eval()
        with torch.no_grad():
            ys_val_pred = model(xs_val)
            val_loss = criterion(ys_val_pred, ys_val)
            val_losses[epoch] = val_loss.item()

        logger.info(f'Epoch [{"0" if epoch+1 < 10 else ""}{epoch+1}/{config.epochs}], Loss: {loss.item():.4f}')
    logger.info(train_losses)
    logger.info(val_losses)
    logger.info(f'[Done] Training. Experiment ID: {config.experiment_id}')


def get_batches(xs, ys, batch_size):
    for i in range(0, len(xs), batch_size):
        yield xs[i:i + batch_size], ys[i:i + batch_size]

def get_device():
    if torch.cuda.is_available():
        logger.info('[Training on GPU]')
        logger.info(f'[Device: {print(torch.cuda.get_device_name(0))}]')
        return torch.device('cuda')
    else:
        logger.info('[Training on CPU]')
        return torch.device('cpu')

def get_model(device, config) -> Autoencoder:
    model = Autoencoder(config.model).to(device)
    return model

def get_train_data(device, config) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: 
    df_xs, df_ys = data_loader.load_train_data()
    np_xs = df_xs.to_numpy()
    np_ys = df_ys.to_numpy()
    xs = np_to_norm_tensor(np_xs).to(device)
    ys = np_to_norm_tensor(np_ys).to(device)

    split_idx = int(xs.size(0) * (1 - config.validation_split))
    xs_train, xs_val = xs[:split_idx], xs[split_idx:]
    ys_train, ys_val = ys[:split_idx], ys[split_idx:]
    return xs_train, ys_train, xs_val, ys_val

def np_to_norm_tensor(np_array: np.ndarray) -> Tensor:
    tensor = torch.tensor(np_array, dtype=torch.float32)
    tensor /= 255.0
    return tensor.reshape(-1, 1, 28, 28)