import uuid
from pydantic import BaseModel
from src.dtos.model_dto import ModelConfig

class TrainConfig(BaseModel):
    model: ModelConfig
    batch_size: int
    epochs: int
    learning_rate: float
    validation_split: float
    model_config = {
        'json_schema_extra': {
            "examples": [
                {
                    'experiment_id': str(uuid.uuid4()),
                    'model': {
                        'encoder_layers': [
                            {'in_channels': 1, 'out_channels': 16, 'kernel_size': 3, 'stride': 2, 'padding': 1, 'activation': 'relu'}, 
                            {'in_channels': 16, 'out_channels': 32, 'kernel_size': 3, 'stride': 2, 'padding': 1, 'activation': 'relu'},
                            {'in_channels': 32, 'out_channels': 64, 'kernel_size': 3, 'stride': 2, 'padding': 1, 'activation': 'relu'} 
                        ],
                        'decoder_layers': [
                            {'in_channels': 64, 'out_channels': 32, 'kernel_size': 3, 'stride': 2, 'padding': 1, 'output_padding': 1, 'activation': 'relu'},
                            {'in_channels': 32, 'out_channels': 16, 'kernel_size': 3, 'stride': 2, 'padding': 2, 'output_padding': 1, 'activation': 'relu'},
                            {'in_channels': 16, 'out_channels': 1, 'kernel_size': 3, 'stride': 2, 'padding': 1, 'output_padding': 1, 'activation': 'sigmoid'}  
                        ]
                    },
                    'batch_size': 64,
                    'epochs': 100,
                    'learning_rate': 0.001,
                    'validation_split': 0.05
                }
            ]
        }
    }
        