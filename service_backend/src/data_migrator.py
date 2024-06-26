import numpy as np
from loguru import logger
from src.loaders.data_csv_loader import load_train_data, load_test_data
from src.loaders.data_db_loader import insert_train_samples, remove_train_samples, insert_test_samples, remove_test_samples
from src.utilities.environment import Environment
from src.watermark.watermark_controller import add_watermarks

def data_migration():
    ys_train, _ = load_train_data()
    ys_train: np.ndarray = ys_train.values
    xs_train: np.ndarray = add_watermarks(ys_train)
    remove_train_samples()
    insert_train_samples(xs_train, ys_train)
    
    ys_test: np.ndarray = load_test_data()
    ys_test: np.ndarray = ys_test.values
    xs_test: np.ndarray = add_watermarks(ys_test)
    remove_test_samples()
    insert_test_samples(xs_test, ys_test)
    
if __name__ == "__main__":
    if Environment().RUN_MIGRATION is True:
        logger.info('Migrating datasets...')
        data_migration()