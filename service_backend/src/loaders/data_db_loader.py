import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from src.utilities.environment import Environment
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.mongo_client import MongoClient
from pandas import DataFrame, Series
from loguru import logger

connection_string: str = f'mongodb://db:{Environment().MONGO_DB_PORT}/'
client: MongoClient = MongoClient(connection_string)
db: Database = client[Environment().MONGO_DB_NAME]
train_collection: Collection = db[Environment().MONGO_DB_TRAIN_COLLECTION_NAME]
test_collection: Collection = db[Environment().MONGO_DB_TEST_COLLECTION_NAME]

def load_train_data() -> Tuple[DataFrame, DataFrame]:
    cursor = train_collection.find()
    samples: List[Dict[int, List[int]]] = list(cursor)
    xs: List[int][int] = []
    ys: List[int][int] = []
    for sample in samples:
        xs.append(sample['image'])
        ys.append(sample['image_with_watermark'])
    return pd.DataFrame(xs), pd.DataFrame(ys)

def insert_train_samples(xs: np.ndarray, ys: np.ndarray) -> None:
    logger.info('inserting train samples...')
    samples: List[Dict] = [{'image': label.tolist(), 'image_with_watermark': row.tolist()} for row, label in zip(xs, ys)]
    train_collection.insert_many(samples)
    logger.info('[DONE] inserting train samples')

def remove_train_samples() -> None:
    logger.info('removing train samples')
    train_collection.delete_many({})
    logger.info('[DONE] removing train samples')

def insert_test_samples(xs: np.ndarray, ys: np.ndarray) -> None: 
    logger.info('inserting test samples')
    samples: List[Dict] = [{'image': label.tolist(), 'image_with_watermark': row.tolist()} for row, label in zip(xs, ys)]
    test_collection.insert_many(samples)
    logger.info('[DONE] inserting test samples')

def remove_test_samples() -> None:
    logger.info('removing test samples')
    test_collection.delete_many({})
    logger.info('[DONE] removing test samples')