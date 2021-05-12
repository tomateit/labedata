from dataset import Dataset
from contextlib import contextmanager
import pandas as pd
from typing import Union

class CSVDataset(Dataset):
    @contextmanager
    def __get_dataset(self)-> pd.DataFrame:
        #TODO line-wise CSV reading
        try:
            dataset = pd.read_csv(self.output_path)
            yield dataset
        finally:
            #? wut
            del dataset

    def next_entity_for_user_id(self, user_id):
        if self.user_based_labeling:
            # 1. ensure dataset is ready for user-based labeling
            # i.e. it has column user_id
            column_name = self.user_id_to_colname(user_id)
            with self.__get_dataset() as dataset:
                if column_name not in dataset.cols:
                    dataset[column_name] = pd.NA
                return 
        else:
            return db.execute(
                f"SELECT X, label\
                FROM {self.tablename} WHERE assessed IS NULL"
            ).fetchone()