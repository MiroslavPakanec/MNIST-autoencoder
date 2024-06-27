import torch.nn as nn
from src.dtos.model_dto import ModelConfig
from src.utilities.exceptions import ModelConfigException

class Autoencoder(nn.Module):
    def __init__(self, model_config: ModelConfig):
        super(Autoencoder, self).__init__()
        self.encoder = build_encoder(model_config)
        self.decoder = build_decoder(model_config)
    
    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x

def build_encoder(model_config: ModelConfig):
    layers = []
    for encoder_layer in model_config.encoder_layers:
        layers.append(nn.Conv2d(encoder_layer.in_channels, encoder_layer.out_channels, kernel_size=encoder_layer.kernel_size, stride=encoder_layer.stride, padding=encoder_layer.padding))
        layers.append(build_activation_layer(encoder_layer.activation))
    encoder =  nn.Sequential(*layers)
    return encoder

def build_decoder(model_config: ModelConfig):
    layers = []
    for decoder_layer in model_config.decoder_layers:
        layers.append(nn.ConvTranspose2d(decoder_layer.in_channels, decoder_layer.out_channels, kernel_size=decoder_layer.kernel_size, stride=decoder_layer.stride, padding=decoder_layer.padding, output_padding=decoder_layer.output_padding))
        layers.append(build_activation_layer(decoder_layer.activation))
    decoder =  nn.Sequential(*layers)
    return decoder

def build_activation_layer(activation_key: str):
    if activation_key.lower() == 'relu':
        return nn.ReLU()
    if activation_key.lower() == 'sigmoid':
        return nn.Sigmoid()
    raise ModelConfigException(f'Unknown activation key {activation_key.lower()}')

